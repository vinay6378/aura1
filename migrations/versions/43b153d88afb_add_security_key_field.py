"""add_security_key_field

Revision ID: 43b153d88afb
Revises: feace478ed95
Create Date: 2026-01-26 09:25:06.395039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43b153d88afb'
down_revision = 'feace478ed95'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('security_key', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('users', 'security_key')
