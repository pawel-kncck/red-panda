"""Add Red Panda models

Revision ID: add_red_panda_models
Revises: remove_items_table
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'add_red_panda_models'
down_revision = 'remove_items_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add API key fields to user table
    op.add_column('user', sa.Column('api_keys', sa.JSON(), nullable=False, server_default='{}'))
    op.add_column('user', sa.Column('api_usage', sa.JSON(), nullable=False, server_default='{}'))
    
    # Create conversation table
    op.create_table('conversation',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('last_message_preview', sa.String(length=500), nullable=True),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('message_count', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversation_user_id'), 'conversation', ['user_id'], unique=False)
    op.create_index(op.f('ix_conversation_created_at'), 'conversation', ['created_at'], unique=False)
    
    # Create codeblock table (CORE FEATURE)
    op.create_table('codeblock',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('language', sa.String(length=20), nullable=False, server_default='python'),
        sa.Column('executed_successfully', sa.Boolean(), nullable=True),
        sa.Column('conversation_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('imports', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('functions_defined', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('variables_created', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('tags', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('parent_version_id', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_version_id'], ['codeblock.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_codeblock_user_id'), 'codeblock', ['user_id'], unique=False)
    op.create_index(op.f('ix_codeblock_conversation_id'), 'codeblock', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_codeblock_created_at'), 'codeblock', ['created_at'], unique=False)
    
    # Create message table
    op.create_table('message',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('conversation_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('code_block_ids', sa.JSON(), nullable=False, server_default='[]'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_conversation_id'), 'message', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_message_created_at'), 'message', ['created_at'], unique=False)
    
    # Create file table
    op.create_table('file',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('storage_path', sa.String(length=500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('file_metadata', sa.JSON(), nullable=False, server_default='{}'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_user_id'), 'file', ['user_id'], unique=False)
    op.create_index(op.f('ix_file_uploaded_at'), 'file', ['uploaded_at'], unique=False)


def downgrade() -> None:
    # Drop all Red Panda tables
    op.drop_index(op.f('ix_file_uploaded_at'), table_name='file')
    op.drop_index(op.f('ix_file_user_id'), table_name='file')
    op.drop_table('file')
    
    op.drop_index(op.f('ix_message_created_at'), table_name='message')
    op.drop_index(op.f('ix_message_conversation_id'), table_name='message')
    op.drop_table('message')
    
    op.drop_index(op.f('ix_codeblock_created_at'), table_name='codeblock')
    op.drop_index(op.f('ix_codeblock_conversation_id'), table_name='codeblock')
    op.drop_index(op.f('ix_codeblock_user_id'), table_name='codeblock')
    op.drop_table('codeblock')
    
    op.drop_index(op.f('ix_conversation_created_at'), table_name='conversation')
    op.drop_index(op.f('ix_conversation_user_id'), table_name='conversation')
    op.drop_table('conversation')
    
    # Remove API key fields from user table
    op.drop_column('user', 'api_usage')
    op.drop_column('user', 'api_keys')