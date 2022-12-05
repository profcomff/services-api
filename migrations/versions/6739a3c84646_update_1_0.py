"""Update 1.0

Revision ID: 6739a3c84646
Revises: 
Create Date: 2022-12-02 16:02:15.329952

"""
from alembic import op
import sqlalchemy as sa


revision = '6739a3c84646'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('button')
    op.drop_table('category')


def downgrade():
    op.create_table('category',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('category_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='category_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('button',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('icon', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name='buttons_category_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='buttons_pkey')
    )
