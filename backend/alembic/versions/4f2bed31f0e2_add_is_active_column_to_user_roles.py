"""add_is_active_column_to_user_roles

Revision ID: 4f2bed31f0e2
Revises: 2b96a20dd9bd
Create Date: 2025-09-04 18:00:50.659857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f2bed31f0e2'
down_revision = '2b96a20dd9bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_active column to user_roles table
    op.add_column('user_roles', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    
    # Add indexes for better performance
    op.create_index('ix_user_roles_user_id', 'user_roles', ['user_id'])
    op.create_index('ix_user_roles_role_id', 'user_roles', ['role_id'])
    op.create_index('ix_user_roles_assigned_at', 'user_roles', ['assigned_at'])
    op.create_index('ix_user_roles_is_active', 'user_roles', ['is_active'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_user_roles_is_active', table_name='user_roles')
    op.drop_index('ix_user_roles_assigned_at', table_name='user_roles')
    op.drop_index('ix_user_roles_role_id', table_name='user_roles')
    op.drop_index('ix_user_roles_user_id', table_name='user_roles')
    
    # Drop is_active column
    op.drop_column('user_roles', 'is_active')
