"""remove_security_key_field

Revision ID: remove_security_key
Revises: 43b153d88afb
Create Date: 2026-01-26 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'remove_security_key'
down_revision = '43b153d88afb'
branch_labels = None
depends_on = None


def upgrade():
    # Remove the security_key column from users table
    op.drop_column('users', 'security_key')


def downgrade():
    # Add the security_key column back
    op.add_column('users', sa.Column('security_key', sa.String(length=255), nullable=True))
