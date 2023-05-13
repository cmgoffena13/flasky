import time
from rq import get_current_job
from app import create_app, db
from app.models import Task, User, Post
import sys
import json
from flask import render_template
from app.email import send_email


app = create_app()
app.app_context().push()


def example(seconds):
    job = get_current_job()
    print("Starting Task")
    for index in range(seconds):
        job.meta["progress"] = 100.0 * index / seconds
        job.save_meta()
        print(index)
        time.sleep(1)
    job.meta["progress"] = 100
    job.save_meta()
    print("Task Completed")


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta["progress"] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.users.add_notification(
            name="task_progress", data={"task_id": job.get_id(), "progress": progress}
        )

        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        total_posts = user.posts.count()
        for index, post in enumerate(
            user.posts.order_by(Post.timestamp.asc()), start=0
        ):
            data.append(
                {"body": post.body, "timestamp": post.timestamp.isoformat() + "Z"}
            )
            time.sleep(5)
            index += 1
            _set_task_progress(100 * index // total_posts)

        send_email(
            "[Flasky] Your blog posts",
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email],
            text_body=render_template("email/export_posts.txt", user=user),
            html_body=render_template("email/export_posts.html", user=user),
            attachments=[
                (
                    "posts.json",
                    "application/json",
                    json.dumps({"posts": data}, indent=4),
                )
            ],
            sync=True,
        )
    except:
        app.logger.error("Unhandled exception", exc_info=sys.exc_info())
    finally:
        _set_task_progress(100)
