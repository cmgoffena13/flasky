import jwt
import json
from app import db, login
from app.search import add_to_index, remove_from_index, query_index
from sqlalchemy.dialects.postgresql import *
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
from flask import current_app, url_for
from datetime import datetime
import redis
import rq


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page, error_out=False)

        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page+1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page-1, per_page=per_page, **kwargs) if resources.has_prev else None 
            }
        }
        return data

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(index=cls.__tablename__, query=expression, page=page, per_page=per_page)
        if total == 0:
            return cls.query.filter_by(__primarykey__=0), 0
        when = []
        for index in range(len(ids)):
            when.append((ids[index], index))
        pk_map = cls.__primarykey__
        pk = getattr(cls, pk_map)
        return cls.query.filter(pk.in_(ids)).order_by(db.case(when, value=pk)), total
    
    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(index=obj.__tablename__, model=obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(index=obj.__table__name, model=obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(index=obj.__tablename__, model=obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(index=cls.__tablename__, model=obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


# No data other than foreign keys, so not defined as a model
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.user_id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.user_id'))
                     )


class User(PaginatedAPIMixin, UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(INTEGER, primary_key=True)
    username = db.Column(VARCHAR(64), index=True, unique=True)
    email = db.Column(VARCHAR(120), index=True, unique=True)
    password_hash = db.Column(VARCHAR(128))
    created_on = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now()) # this doesn't generate in alembic correctly..
    about_me = db.Column(VARCHAR(140))
    last_seen = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    last_message_read_time = db.Column(TIMESTAMP(timezone=True))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User', 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == user_id),
                               secondaryjoin=(followers.c.followed_id == user_id),
                               backref=db.backref('followers', lazy='dynamic'), 
                               lazy='dynamic')
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    notifications = db.relationship('Notification', backref='users', lazy='dynamic')
    tasks = db.relationship('Task', backref='users', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.user_id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(user_id)
    
    def get_id(self):
        return self.user_id

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.user_id).count() > 0 # Could be == 1...

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.user_id
        )
        own = Post.query.filter_by(user_id = self.user_id)
        return followed.union(own).order_by(Post.timestamp.desc())
    
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient_id=self.user_id).filter(Message.timestamp > last_read_time).count()
    
    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), users=self) # user=self; user = User instance
        db.session.add(n)
        return n
    
    def launch_task(self, name, description, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name, self.user_id, *args, **kwargs)
        task = Task(task_id=rq_job.get_id(), name=name, description=description, users=self) # user=self; user = User instance
        db.session.add(task)
        return task
    
    def get_tasks_in_progress(self):
        return Task.query.filter_by(user_id=self.user_id, complete=False).all()
    
    def get_task_in_progress(self, name):
        return Task.query.filter_by(name=name, user_id=self.user_id, complete=False).first()
    
    def to_dict(self, include_email=False):
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z', #utc?
            'about_me': self.about_me,
            'post_count': self.posts.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            '_links': {
                'self': url_for('users.API_User', user_id=self.user_id),
                'followers': url_for('users.get_followers', user_id=self.user_id),
                'followed': url_for('users.get_followed', user_id=self.user_id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])



@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
class Post(SearchableMixin, db.Model):
    __tablename__ = 'posts'

    __searchable__ = ['body']

    __primarykey__ = 'post_id'  # Used for ElasticSearch, does not support composite keys

    post_id = db.Column(INTEGER, primary_key=True)
    body = db.Column(VARCHAR(4000))
    timestamp = db.Column(TIMESTAMP(timezone=True), index=True, server_default=func.now())
    user_id = db.Column(INTEGER, db.ForeignKey("users.user_id"))
    language = db.Column(VARCHAR(5))

    def __repr__(self):
        return f'<Post {self.body}>'


class Message(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(INTEGER, primary_key=True)
    sender_id = db.Column(INTEGER, db.ForeignKey("users.user_id"))
    recipient_id = db.Column(INTEGER, db.ForeignKey("users.user_id"))
    body = db.Column(VARCHAR(500))
    timestamp = db.Column(TIMESTAMP(timezone=True), index=True, server_default=func.now())

    def __repr__(self):
        return f'<Message {self.body}>'
    

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(BIGINT, primary_key=True)
    name = db.Column(VARCHAR(128), index=True)
    user_id = db.Column(INTEGER, db.ForeignKey('users.user_id'))
    timestamp = db.Column(NUMERIC(16,6), index=True, default=time)
    payload_json = db.Column(VARCHAR)

    def get_data(self):
        return json.loads(str(self.payload_json))
    

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(VARCHAR(36), primary_key=True)
    name = db.Column(VARCHAR(128), index=True)
    description = db.Column(VARCHAR(128))
    user_id = db.Column(INTEGER, db.ForeignKey('users.user_id'))
    complete = db.Column(BOOLEAN, default=False)
    created_on = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.task_id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job
    
    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100
