"""users table

Revision ID: 084c3752872b
Revises: fc5c15a94ff6
Create Date: 2021-04-19 14:26:38.959813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "084c3752872b"
down_revision = "fc5c15a94ff6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("is_admin", sa.Boolean(), nullable=True))
    op.create_index(op.f("ix_user_is_admin"), "user", ["is_admin"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_is_admin"), table_name="user")
    op.drop_column("user", "is_admin")
    # ### end Alembic commands ###