"""questions

Revision ID: 77a2c750d813
Revises: 90c702adeff9
Create Date: 2021-05-04 18:44:51.453358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "77a2c750d813"
down_revision = "90c702adeff9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("attempt", schema=None) as batch_op:
        batch_op.create_foreign_key("fk_q5", "questions", ["question_5_id"], ["question_id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("attempt", schema=None) as batch_op:
        batch_op.drop_constraint("fk_q5", type_="foreignkey")

    # ### end Alembic commands ###
