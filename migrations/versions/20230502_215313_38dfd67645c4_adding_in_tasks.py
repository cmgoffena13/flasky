"""adding in tasks

Revision ID: 38dfd67645c4
Revises: 5ba251f541f5
Create Date: 2023-05-02 21:53:13.525676

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "38dfd67645c4"
down_revision = "5ba251f541f5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tasks",
        sa.Column("task_id", sa.VARCHAR(length=36), nullable=False),
        sa.Column("name", sa.VARCHAR(length=128), nullable=True),
        sa.Column("description", sa.VARCHAR(length=128), nullable=True),
        sa.Column("user_id", sa.INTEGER(), nullable=True),
        sa.Column("complete", sa.BOOLEAN(), nullable=True),
        sa.Column(
            "created_on",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.user_id"], name=op.f("fk_tasks_user_id_users")
        ),
        sa.PrimaryKeyConstraint("task_id", name=op.f("pk_tasks")),
    )
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_tasks_name"), ["name"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_tasks_name"))

    op.drop_table("tasks")
    # ### end Alembic commands ###
