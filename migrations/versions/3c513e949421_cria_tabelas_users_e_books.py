"""cria tabelas users e books

Revision ID: 3c513e949421
Revises:
Create Date: 2024-12-22 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c513e949421'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), sa.Identity(always=False), primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
    )

    # Tabela categories
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), unique=True, nullable=False),
    )

    # Tabela books
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column('upc', sa.String(50), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('rating', sa.Integer()),
        sa.Column('quantity', sa.Integer()),
        sa.Column('availability', sa.Boolean()),
        sa.Column('imagem_url', sa.Text()),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id')),
    )


def downgrade() -> None:
    op.drop_table('books')
    op.drop_table('categories')
    op.drop_table('users')

