"""alter_invoice_table

Revision ID: 2a7dc970dd5b
Revises: 2a7dc970dd5b
Create Date: 2024-12-21 21:06:14.373860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a7dc970dd5b'
down_revision: Union[str, None] = '5e890cec19a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices') as batch_op:
        batch_op.add_column(sa.Column('paid_value', sa.Numeric(), nullable=True))
        batch_op.alter_column('payment_date',
                existing_type=sa.DATE(),
                type_=sa.DateTime(),
                existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices') as batch_op:
        batch_op.drop_column('paid_value')
        batch_op.alter_column('payment_date',
                existing_type=sa.DateTime(),
                type_=sa.DATE(),
                existing_nullable=True)
    # ### end Alembic commands ###
