"""End-to-end numbering fix

Revision ID: d35e88f39f85
Revises: 660bb7891726
Create Date: 2023-04-09 11:28:59.326067

"""
import operator

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd35e88f39f85'
down_revision = '660bb7891726'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    res_c = conn.execute(sa.text("select * from category ORDER BY category.order")).fetchall()
    for category in res_c:
        res_b = conn.execute(
            sa.text(f"select * from button WHERE category_id={category[0]} ORDER BY button.order")
        ).fetchall()
        for i in range(0, len(res_b)):
            conn.execute(
                sa.text(
                    f"""UPDATE "button"
                                        SET "order"={i + 1}, 
                                            "link"='{res_b[i][5]}', 
                                            "type"='{res_b[i][6]}' 
                                        WHERE id={res_b[i][0]}"""
                )
            )


def downgrade():
    k = 0
    conn = op.get_bind()
    res_c = conn.execute(sa.text("select * from category ORDER BY category.order")).fetchall()
    for category in res_c:
        res_b = conn.execute(
            sa.text(f"select * from button WHERE category_id={category[0]} ORDER BY button.order")
        ).fetchall()
        for i in range(0, len(res_b)):
            conn.execute(
                sa.text(
                    f"""UPDATE "button"
                                            SET "order"={k + 1}, 
                                                "link"='{res_b[i][5]}', 
                                                "type"='{res_b[i][6]}' 
                                            WHERE id={res_b[i][0]}"""
                )
            )
            k += 1
