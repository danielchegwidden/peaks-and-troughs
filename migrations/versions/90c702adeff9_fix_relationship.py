"""fix relationship

Revision ID: 90c702adeff9
Revises: fcf7875608a0
Create Date: 2021-04-30 12:30:29.348818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "90c702adeff9"
down_revision = "fcf7875608a0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("attempt", schema=None) as batch_op:
        batch_op.create_foreign_key("fk_q2", "questions", ["question_2_id"], ["question_id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("attempt", schema=None) as batch_op:
        batch_op.drop_constraint("fk_q2", type_="foreignkey")

    # ### end Alembic commands ###
