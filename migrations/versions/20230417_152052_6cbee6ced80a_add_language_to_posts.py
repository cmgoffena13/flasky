"""add language to posts

Revision ID: 6cbee6ced80a
Revises: 336788c3d4ff
Create Date: 2023-04-17 15:20:52.666594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6cbee6ced80a"
down_revision = "336788c3d4ff"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.add_column(sa.Column("language", sa.VARCHAR(length=5), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.drop_column("language")

    # ### end Alembic commands ###
