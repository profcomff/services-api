"""button_scopes

Revision ID: 1bb798899506
Revises: d6b21dcb2c75
Create Date: 2024-04-06 20:47:43.848321

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '1bb798899506'
down_revision = 'd6b21dcb2c75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scope', sa.Column('button_id', sa.Integer(), nullable=True))
    op.add_column('scope', sa.Column('is_required', sa.Boolean(), nullable=True))
    op.alter_column('scope', 'category_id', existing_type=sa.INTEGER(), nullable=True)
    op.create_foreign_key(None, 'scope', 'button', ['button_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'scope', type_='foreignkey')
    op.alter_column('scope', 'category_id', existing_type=sa.INTEGER(), nullable=False)
    op.drop_column('scope', 'is_required')
    op.drop_column('scope', 'button_id')
    # ### end Alembic commands ###
