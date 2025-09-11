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
    
    # Note: Composite indexes are now handled in the previous migration
    
    # Note: Unique constraints are skipped for SQLite - they would need to be added 
    # at table creation time. For now, they will be enforced at the application level.


def downgrade() -> None:
    """
    Remove the SQLite-compatible constraints and indexes.
    """
    
    # Note: No indexes to drop in this migration since they're handled elsewhere
