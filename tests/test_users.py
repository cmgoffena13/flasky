from datetime import datetime, timedelta
from app.models import User, Post
from app import db


class TestUserClass:
    def test_password_hashing(self):
        u = User(username="susan")
        u.set_password("cat")
        assert u.check_password("dog") is False
        assert u.check_password("cat") is True

    def test_avatar(self):
        u = User(username="john", email="john@example.com")
        assert (
            u.avatar(128)
            == "https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128"
        )

    def test_follow(self):
        john = User(username="john", email="john@example.com")
        susan = User(username="susan", email="susan@example.com")
        db.session.add(john)
        db.session.add(susan)
        db.session.commit()
        assert john.followed.all() == []
        assert john.followers.all() == []

        john.follow(susan)
        db.session.commit()
        assert john.is_following(susan) is True
        assert john.followed.count() == 1
        assert john.followed.first().username == "susan"
        assert susan.followers.count() == 1
        assert susan.followers.first().username == "john"

        john.unfollow(susan)
        db.session.commit()
        assert john.is_following(susan) is False
        assert john.followed.count() == 0
        assert susan.followers.count() == 0

    def test_follow_posts(self):
        john = User(username="john", email="john@example.com")
        susan = User(username="susan", email="susan@example.com")
        mary = User(username="mary", email="mary@example.com")
        david = User(username="david", email="david@example.com")
        db.session.add_all([john, susan, mary, david])

        now = datetime.utcnow()
        john_post = Post(
            body="post from john", author=john, timestamp=now + timedelta(seconds=1)
        )
        susan_post = Post(
            body="post from susan", author=susan, timestamp=now + timedelta(seconds=4)
        )
        mary_post = Post(
            body="post from mary", author=mary, timestamp=now + timedelta(seconds=3)
        )
        david_post = Post(
            body="post from david", author=david, timestamp=now + timedelta(seconds=2)
        )
        db.session.add_all([john_post, susan_post, mary_post, david_post])
        db.session.commit()

        john.follow(susan)
        john.follow(david)
        susan.follow(mary)
        mary.follow(david)
        db.session.commit()

        f1 = john.followed_posts().all()
        f2 = susan.followed_posts().all()
        f3 = mary.followed_posts().all()
        f4 = david.followed_posts().all()

        assert f1 == [susan_post, david_post, john_post]  # need correct order
        assert f2 == [susan_post, mary_post]
        assert f3 == [mary_post, david_post]
        assert f4 == [david_post]
