"""order

Revision ID: 6a486347af93
Revises: 670f4caac7dd
Create Date: 2023-02-11 10:18:11.179485

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '6a486347af93'
down_revision = '670f4caac7dd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('button', sa.Column('order', sa.Integer(), nullable=True))
    op.add_column('button', sa.Column('link', sa.String(), nullable=True))
    op.add_column('button', sa.Column('type', sa.String(), nullable=True))
    conn = op.get_bind()
    res = conn.execute(sa.text("select * from button")).fetchall()
    for i in range(0, len(res)):
        conn.execute(
            sa.text(
                f"""UPDATE "button"
                                 SET "order"={i + 1}, 
                                     "link"=#', 
                                     "type"='inapp'
                                 WHERE id={res[i][0]}"""
            )
        )
    op.alter_column('button', 'order', nullable=False)
    op.alter_column('button', 'link', nullable=False)
    op.alter_column('button', 'type', nullable=False)
    op.alter_column('button', 'name', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('button', 'category_id', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('button', 'icon', existing_type=sa.VARCHAR(), nullable=False)
    op.add_column('category', sa.Column('order', sa.Integer(), nullable=True))
    res_c = conn.execute(sa.text("select id from category")).fetchall()
    for i in range(0, len(res_c)):
        conn.execute(
            sa.text(
                f"""UPDATE "category"
                                     SET "order"={i + 1} 
                                     WHERE id={res_c[i][0]}"""
            )
        )
    op.alter_column('category', 'order', nullable=False)
    op.alter_column('category', 'name', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('category', 'type', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('button', 'order', nullable=False)


def downgrade():
    op.alter_column('category', 'type', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('category', 'name', existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column('category', 'order')
    op.alter_column('button', 'icon', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('button', 'category_id', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('button', 'name', existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column('button', 'type')
    op.drop_column('button', 'link')
    op.drop_column('button', 'order')
