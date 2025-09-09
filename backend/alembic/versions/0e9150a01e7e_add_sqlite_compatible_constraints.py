"""add_sqlite_compatible_constraints

Revision ID: 0e9150a01e7e
Revises: 7f91e9655315
Create Date: 2025-09-09 11:36:07.662517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e9150a01e7e'
down_revision = '7f91e9655315'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add SQLite-compatible constraints and indexes for better data integrity and performance.
    
    This migration adds:
    1. Additional indexes for query performance
    2. Unique constraints where SQLite supports them
    3. Composite indexes for common query patterns
    """
    
    # Add composite indexes for common query patterns
    op.create_index(
        'ix_scores_user_analysis_type',
        'scores',
        ['user_id', 'analysis_type', 'is_active']
    )
    
    op.create_index(
        'ix_scores_resume_analysis_type',
        'scores',
        ['resume_id', 'analysis_type', 'is_active']
    )
    
    op.create_index(
        'ix_scores_user_analysis_date',
        'scores',
        ['user_id', 'analysis_date', 'is_active']
    )
    
    op.create_index(
        'ix_resumes_user_created',
        'resumes',
        ['user_id', 'created_at', 'is_active']
    )
    
    op.create_index(
        'ix_user_roles_user_active',
        'user_roles',
        ['user_id', 'is_active', 'assigned_at']
    )
    
    op.create_index(
        'ix_user_roles_role_active',
        'user_roles',
        ['role_id', 'is_active', 'assigned_at']
    )
    
    # Add index for role name lookups (case-insensitive)
    op.create_index(
        'ix_roles_name_lower',
        'roles',
        [sa.text('LOWER(name)')]
    )
    
    # Add index for user email lookups (case-insensitive)
    op.create_index(
        'ix_users_email_lower',
        'users',
        [sa.text('LOWER(email)')]
    )
    
    # Add unique constraint to prevent duplicate user-role assignments (SQLite compatible)
    op.create_unique_constraint(
        'uq_user_roles_user_role_active',
        'user_roles',
        ['user_id', 'role_id', 'is_active']
    )
    
    # Add unique constraint to prevent duplicate active resumes per user (SQLite compatible)
    op.create_unique_constraint(
        'uq_resumes_user_title_active',
        'resumes',
        ['user_id', 'title', 'is_active']
    )


def downgrade() -> None:
    """
    Remove the SQLite-compatible constraints and indexes.
    """
    
    # Drop unique constraints
    op.drop_constraint('uq_resumes_user_title_active', 'resumes', type_='unique')
    op.drop_constraint('uq_user_roles_user_role_active', 'user_roles', type_='unique')
    
    # Drop composite indexes
    op.drop_index('ix_users_email_lower', table_name='users')
    op.drop_index('ix_roles_name_lower', table_name='roles')
    op.drop_index('ix_user_roles_role_active', table_name='user_roles')
    op.drop_index('ix_user_roles_user_active', table_name='user_roles')
    op.drop_index('ix_resumes_user_created', table_name='resumes')
    op.drop_index('ix_scores_user_analysis_date', table_name='scores')
    op.drop_index('ix_scores_resume_analysis_type', table_name='scores')
    op.drop_index('ix_scores_user_analysis_type', table_name='scores')
