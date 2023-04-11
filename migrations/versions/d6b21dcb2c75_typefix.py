"""typefix

Revision ID: d6b21dcb2c75
Revises: d35e88f39f85
Create Date: 2023-04-11 14:21:54.007129

"""
import sqlalchemy as sa
from alembic import op

from services_backend.models.database import Type


# revision identifiers, used by Alembic.
revision = 'd6b21dcb2c75'
down_revision = 'd35e88f39f85'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    res_b = conn.execute(sa.text("select * from button")).fetchall()
    for i in range(len(res_b)):
        conn.execute(
            sa.text(
                f"""UPDATE "button"
                    SET "type"=UPPER('{res_b[i][6]}')
                    WHERE id={res_b[i][0]}"""
            )
        )


def downgrade():
    conn = op.get_bind()
    res_b = conn.execute(sa.text("select * from button")).fetchall()
    for i in range(len(res_b)):
        conn.execute(
            sa.text(
                f"""UPDATE "button"
                        SET "type"=LOWER('{res_b[i][6]}')
                        WHERE id={res_b[i][0]}"""
            )
        )
