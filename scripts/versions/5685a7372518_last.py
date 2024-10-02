"""lol

Revision ID: 5685a7372518
Revises: d5a1e810d3ae
Create Date: 2024-10-02 20:11:19.323876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5685a7372518'
down_revision: Union[str, None] = 'd5a1e810d3ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Order',
    sa.Column('id', sa.VARCHAR(length=5), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('IN_PROGRESS', 'SHIPPED', 'DELIVERED', name='orderstatus'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Product',
    sa.Column('id', sa.VARCHAR(length=5), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('amount_in_stock', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('OrderItem',
    sa.Column('id', sa.VARCHAR(length=5), nullable=False),
    sa.Column('order_id', sa.VARCHAR(length=5), nullable=False),
    sa.Column('product_id', sa.VARCHAR(length=5), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['Order.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['Product.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('OrderItem')
    op.drop_table('Product')
    op.drop_table('Order')
    # ### end Alembic commands ###
