"""attempt methods

Revision ID: fcf7875608a0
Revises: c397a5d139df
Create Date: 2021-04-30 12:25:48.189759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fcf7875608a0"
down_revision = "c397a5d139df"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("attempt", schema=None) as batch_op:
        batch_op.create_foreign_key("fk_q2", "questions", ["question_2_id"], ["question_id"])
        batch_op.create_foreign_key("fk_q4", "questions", ["question_4_id"], ["question_id"])
        batch_op.create_foreign_key("fk_users_attempt", "users", ["user_id"], ["id"])
        batch_op.create_foreign_key("fk_q3", "questions", ["question_3_id"], ["question_id"])
        batch_op.create_foreign_key("fk_q1", "questions", ["question_1_id"], ["question_id"])
        batch_op.create_foreign_key("fk_q2", "questions", ["question_5_id"], ["question_id"])

    with op.batch_alter_table("progress", schema=None) as batch_op:
        batch_op.create_foreign_key("fk_users_progress", "users", ["user_id"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("progress", schema=None) as batch_op:
        batch_op.drop_constraint("fk_users_progress", type_="foreignkey")

    with op.batch_alter_table("attempt", schema=None) as batch_op:
        batch_op.drop_constraint("fk_q1", type_="foreignkey")
        batch_op.drop_constraint("fk_q2", type_="foreignkey")
        batch_op.drop_constraint("fk_q3", type_="foreignkey")
        batch_op.drop_constraint("fk_q4", type_="foreignkey")
        batch_op.drop_constraint("fk_q5", type_="foreignkey")
        batch_op.drop_constraint("fk_users_attempt", type_="foreignkey")

    # ### end Alembic commands ###
