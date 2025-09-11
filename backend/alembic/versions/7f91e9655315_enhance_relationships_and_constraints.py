"""enhance_relationships_and_constraints

Revision ID: 7f91e9655315
Revises: 4f2bed31f0e2
Create Date: 2025-09-09 11:34:05.633143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f91e9655315'
down_revision = '4f2bed31f0e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Enhance relationships and constraints for better data integrity and performance.
    
    This migration adds:
    1. Additional indexes for query performance
    2. Composite indexes for common query patterns
    
    Note: Unique constraints and check constraints are skipped for SQLite compatibility.
    They should be enforced at the application level for SQLite.
    """
    
    # Skip constraints for SQLite - they need to be defined at table creation time
    # or enforced at the application level
    
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


def downgrade() -> None:
    """
    Remove the enhanced relationships and constraints.
    """
    
    # Drop composite indexes
    op.drop_index('ix_users_email_lower', table_name='users')
    op.drop_index('ix_roles_name_lower', table_name='roles')
    op.drop_index('ix_user_roles_role_active', table_name='user_roles')
    op.drop_index('ix_user_roles_user_active', table_name='user_roles')
    op.drop_index('ix_resumes_user_created', table_name='resumes')
    op.drop_index('ix_scores_user_analysis_date', table_name='scores')
    op.drop_index('ix_scores_resume_analysis_type', table_name='scores')
    op.drop_index('ix_scores_user_analysis_type', table_name='scores')
    
    # Note: Constraints were skipped for SQLite compatibility
