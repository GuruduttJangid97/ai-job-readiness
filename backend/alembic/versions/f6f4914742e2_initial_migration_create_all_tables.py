"""Initial migration - create all tables

Revision ID: f6f4914742e2
Revises: 
Create Date: 2025-09-01 22:38:16.216742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6f4914742e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table (with IF NOT EXISTS check)
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) NOT NULL,
            email VARCHAR(320) NOT NULL,
            hashed_password VARCHAR(1024) NOT NULL,
            is_active BOOLEAN DEFAULT true NOT NULL,
            is_superuser BOOLEAN DEFAULT false NOT NULL,
            is_verified BOOLEAN DEFAULT false NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone VARCHAR(20),
            bio TEXT,
            profile_picture_url VARCHAR(500),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE,
            PRIMARY KEY (id),
            UNIQUE (email)
        )
    """)
    
    # Create roles table (with IF NOT EXISTS check)
    op.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            permissions JSONB DEFAULT '[]'::jsonb,
            is_active BOOLEAN DEFAULT true NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """)
    
    # Create user_roles table (with IF NOT EXISTS check)
    op.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(36) NOT NULL,
            role_id INTEGER NOT NULL,
            assigned_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
            assigned_by VARCHAR(36),
            is_active BOOLEAN DEFAULT true NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
            UNIQUE (user_id, role_id)
        )
    """)
    
    # Create resumes table (with IF NOT EXISTS check)
    op.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(36) NOT NULL,
            title VARCHAR(200) NOT NULL,
            file_path VARCHAR(500),
            file_name VARCHAR(255),
            file_size BIGINT,
            file_type VARCHAR(50),
            summary TEXT,
            experience_years DECIMAL(3,1),
            education_level VARCHAR(100),
            skills JSONB DEFAULT '[]'::jsonb,
            languages JSONB DEFAULT '[]'::jsonb,
            is_active BOOLEAN DEFAULT true NOT NULL,
            is_public BOOLEAN DEFAULT true NOT NULL,
            last_analyzed TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Create scores table (with IF NOT EXISTS check)
    op.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(36) NOT NULL,
            resume_id INTEGER NOT NULL,
            analysis_type VARCHAR(50) NOT NULL,
            job_title VARCHAR(200),
            company VARCHAR(200),
            overall_score DECIMAL(5,2) NOT NULL,
            skill_score DECIMAL(5,2),
            experience_score DECIMAL(5,2),
            education_score DECIMAL(5,2),
            skill_matches JSONB DEFAULT '[]'::jsonb,
            skill_gaps JSONB DEFAULT '[]'::jsonb,
            recommendations TEXT,
            analysis_details JSONB DEFAULT '{}'::jsonb,
            is_active BOOLEAN DEFAULT true NOT NULL,
            analysis_date TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
        )
    """)
    
    # Create indexes if they don't exist
    op.execute("CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON user_roles(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_user_roles_role_id ON user_roles(role_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_scores_user_id ON scores(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_scores_resume_id ON scores(resume_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_scores_analysis_type ON scores(analysis_type)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active)")


def downgrade() -> None:
    # Drop indexes
    op.execute("DROP INDEX IF EXISTS idx_scores_analysis_type")
    op.execute("DROP INDEX IF EXISTS idx_scores_resume_id")
    op.execute("DROP INDEX IF EXISTS idx_scores_user_id")
    op.execute("DROP INDEX IF EXISTS idx_resumes_user_id")
    op.execute("DROP INDEX IF EXISTS idx_user_roles_role_id")
    op.execute("DROP INDEX IF EXISTS idx_user_roles_user_id")
    op.execute("DROP INDEX IF EXISTS idx_users_email")
    op.execute("DROP INDEX IF EXISTS idx_users_created_at")
    op.execute("DROP INDEX IF EXISTS idx_users_is_active")
    
    # Drop tables in reverse order
    op.execute("DROP TABLE IF EXISTS scores CASCADE")
    op.execute("DROP TABLE IF EXISTS resumes CASCADE")
    op.execute("DROP TABLE IF EXISTS user_roles CASCADE")
    op.execute("DROP TABLE IF EXISTS roles CASCADE")
    op.execute("DROP TABLE IF EXISTS users CASCADE")