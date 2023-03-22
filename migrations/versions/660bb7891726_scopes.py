"""Scopes

Revision ID: 660bb7891726
Revises: 6a486347af93
Create Date: 2023-03-16 14:38:26.163590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '660bb7891726'
down_revision = '6a486347af93'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'scope',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['category_id'],
            ['category.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('scope')
