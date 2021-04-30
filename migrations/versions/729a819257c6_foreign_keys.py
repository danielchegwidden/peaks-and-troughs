"""foreign keys

Revision ID: 729a819257c6
Revises: 337d787f752a
Create Date: 2021-04-30 11:53:02.513673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "729a819257c6"
down_revision = "337d787f752a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, "attempt", "users", ["user_id"], ["id"])
    op.create_foreign_key(None, "attempt", "questions", ["question_5_id"], ["question_id"])
    op.create_foreign_key(None, "attempt", "questions", ["question_4_id"], ["question_id"])
    op.create_foreign_key(None, "attempt", "questions", ["question_3_id"], ["question_id"])
    op.create_foreign_key(None, "attempt", "questions", ["question_2_id"], ["question_id"])
    op.create_foreign_key(None, "attempt", "questions", ["question_1_id"], ["question_id"])
    op.create_foreign_key(None, "progress", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "progress", type_="foreignkey")
    op.drop_constraint(None, "attempt", type_="foreignkey")
    op.drop_constraint(None, "attempt", type_="foreignkey")
    op.drop_constraint(None, "attempt", type_="foreignkey")
    op.drop_constraint(None, "attempt", type_="foreignkey")
    op.drop_constraint(None, "attempt", type_="foreignkey")
    op.drop_constraint(None, "attempt", type_="foreignkey")
    # ### end Alembic commands ###
