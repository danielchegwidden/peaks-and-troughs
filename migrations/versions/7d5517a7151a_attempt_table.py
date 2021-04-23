"""attempt table

Revision ID: 7d5517a7151a
Revises: 084c3752872b
Create Date: 2021-04-19 16:13:28.650849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7d5517a7151a"
down_revision = "084c3752872b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "attempt",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("question_1", sa.Boolean(), nullable=True),
        sa.Column("question_2", sa.Boolean(), nullable=True),
        sa.Column("question_3", sa.Boolean(), nullable=True),
        sa.Column("question_4", sa.Boolean(), nullable=True),
        sa.Column("question_5", sa.Boolean(), nullable=True),
        sa.Column("result", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(op.f("ix_attempt_question_1"), "attempt", ["question_1"], unique=False)
    op.create_index(op.f("ix_attempt_question_2"), "attempt", ["question_2"], unique=False)
    op.create_index(op.f("ix_attempt_question_3"), "attempt", ["question_3"], unique=False)
    op.create_index(op.f("ix_attempt_question_4"), "attempt", ["question_4"], unique=False)
    op.create_index(op.f("ix_attempt_question_5"), "attempt", ["question_5"], unique=False)
    op.create_table(
        "learn_progress",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("stocks_a", sa.Boolean(), nullable=True),
        sa.Column("stocks_b", sa.Boolean(), nullable=True),
        sa.Column("deriv_a", sa.Boolean(), nullable=True),
        sa.Column("deriv_b", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(op.f("ix_learn_progress_deriv_a"), "learn_progress", ["deriv_a"], unique=False)
    op.create_index(op.f("ix_learn_progress_deriv_b"), "learn_progress", ["deriv_b"], unique=False)
    op.create_index(
        op.f("ix_learn_progress_stocks_a"), "learn_progress", ["stocks_a"], unique=False
    )
    op.create_index(
        op.f("ix_learn_progress_stocks_b"), "learn_progress", ["stocks_b"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_learn_progress_stocks_b"), table_name="learn_progress")
    op.drop_index(op.f("ix_learn_progress_stocks_a"), table_name="learn_progress")
    op.drop_index(op.f("ix_learn_progress_deriv_b"), table_name="learn_progress")
    op.drop_index(op.f("ix_learn_progress_deriv_a"), table_name="learn_progress")
    op.drop_table("learn_progress")
    op.drop_index(op.f("ix_attempt_question_5"), table_name="attempt")
    op.drop_index(op.f("ix_attempt_question_4"), table_name="attempt")
    op.drop_index(op.f("ix_attempt_question_3"), table_name="attempt")
    op.drop_index(op.f("ix_attempt_question_2"), table_name="attempt")
    op.drop_index(op.f("ix_attempt_question_1"), table_name="attempt")
    op.drop_table("attempt")
    # ### end Alembic commands ###
