"""create_relationship_invoice_and_user

Revision ID: 5e890cec19a9
Revises: 8b54d39d23da
Create Date: 2024-12-21 20:49:18.506991

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5e890cec19a9"
down_revision: Union[str, None] = "8b54d39d23da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("invoices") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("invoices", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("invoices") as batch_op:
        batch_op.drop_constraint(None, "invoices", type_="foreignkey")
        batch_op.drop_column("invoices", "user_id")
    # ### end Alembic commands ###
