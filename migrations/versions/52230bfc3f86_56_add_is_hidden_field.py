"""#56_add_is_hidden_field

Revision ID: 52230bfc3f86
Revises: 1bb798899506
Create Date: 2024-07-29 20:05:34.777852

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '52230bfc3f86'
down_revision = '1bb798899506'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('button', sa.Column('is_hidden', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('button', 'is_hidden')
    # ### end Alembic commands ###
