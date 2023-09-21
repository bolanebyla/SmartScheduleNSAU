"""Create schema `lessons_schedule`

Revision ID: f90943577f8d
Revises:
Create Date: 2023-09-21 01:49:07.239347+00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f90943577f8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE SCHEMA IF NOT EXISTS lessons_schedule')


def downgrade():
    op.execute('DROP SCHEMA IF EXISTS lessons_schedule')
