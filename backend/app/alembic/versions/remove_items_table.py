"""Remove items table

Revision ID: remove_items_table
Revises: 1a31ce608336
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'remove_items_table'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the item table
    op.drop_table('item')


def downgrade() -> None:
    # Recreate the item table
    op.create_table('item',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('owner_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )