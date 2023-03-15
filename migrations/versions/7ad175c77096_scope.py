"""Scope

Revision ID: 7ad175c77096
Revises: 6a486347af93
Create Date: 2023-03-11 21:25:59.030196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ad175c77096'
down_revision = '6a486347af93'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('category', sa.Column('read_scope', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('category_read_scope_fkey', 'category', 'scope', ['read_scope'], ['id'])


def downgrade():
    op.drop_constraint('category_read_scope_fkey', 'category', type_='foreignkey')
    op.drop_column('category', 'read_scope')