from app import create_app, db, cli
from app.models import User, Post, Message, Notification


app = create_app()
cli.register(app=app)


# This initializes the below objects when you use the "flask shell" command for easier use
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message, 'Notification': Notification}