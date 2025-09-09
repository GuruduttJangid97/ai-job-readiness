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
    1. Unique constraints for data integrity
    2. Additional indexes for query performance
    3. Check constraints for data validation
    4. Composite indexes for common query patterns
    """
    
    # Add unique constraint to prevent duplicate user-role assignments
    op.create_unique_constraint(
        'uq_user_roles_user_role_active',
        'user_roles',
        ['user_id', 'role_id', 'is_active'],
        name='uq_user_roles_user_role_active'
    )
    
    # Add unique constraint to prevent duplicate active resumes per user
    op.create_unique_constraint(
        'uq_resumes_user_title_active',
        'resumes',
        ['user_id', 'title', 'is_active'],
        name='uq_resumes_user_title_active'
    )
    
    # Add check constraints for data validation
    op.create_check_constraint(
        'ck_scores_overall_score_range',
        'scores',
        'overall_score >= 0 AND overall_score <= 100'
    )
    
    op.create_check_constraint(
        'ck_scores_skill_score_range',
        'scores',
        'skill_score IS NULL OR (skill_score >= 0 AND skill_score <= 100)'
    )
    
    op.create_check_constraint(
        'ck_scores_experience_score_range',
        'scores',
        'experience_score IS NULL OR (experience_score >= 0 AND experience_score <= 100)'
    )
    
    op.create_check_constraint(
        'ck_scores_education_score_range',
        'scores',
        'education_score IS NULL OR (education_score >= 0 AND education_score <= 100)'
    )
    
    op.create_check_constraint(
        'ck_resumes_experience_years_range',
        'resumes',
        'experience_years IS NULL OR (experience_years >= 0 AND experience_years <= 100)'
    )
    
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
    
    # Drop check constraints
    op.drop_constraint('ck_resumes_experience_years_range', 'resumes', type_='check')
    op.drop_constraint('ck_scores_education_score_range', 'scores', type_='check')
    op.drop_constraint('ck_scores_experience_score_range', 'scores', type_='check')
    op.drop_constraint('ck_scores_skill_score_range', 'scores', type_='check')
    op.drop_constraint('ck_scores_overall_score_range', 'scores', type_='check')
    
    # Drop unique constraints
    op.drop_constraint('uq_resumes_user_title_active', 'resumes', type_='unique')
    op.drop_constraint('uq_user_roles_user_role_active', 'user_roles', type_='unique')
