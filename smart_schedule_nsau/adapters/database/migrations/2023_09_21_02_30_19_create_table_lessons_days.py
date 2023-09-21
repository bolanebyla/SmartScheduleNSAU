"""Create table `lessons_days`

Revision ID: cfbe796b18c1
Revises: f90943577f8d
Create Date: 2023-09-21 02:30:19.212846+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'cfbe796b18c1'
down_revision = 'f90943577f8d'
branch_labels = None
depends_on = None

metadata = sa.MetaData()
schema = 'lessons_schedule'

WeekParitiesEnum = sa.Enum(
    'четная',
    'нечетная',
    name='week_parities',
    create_constraint=True,
    validate_strings=True,
    metadata=metadata,
    schema=schema,
)


def upgrade():
    WeekParitiesEnum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'lessons_days',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('week_parity', WeekParitiesEnum, nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_lessons_days')),
        schema=schema,
    )
    op.create_index(
        'idx_lessons_days_number_week_parity',
        'lessons_days',
        ['number', 'week_parity'],
        schema=schema,
    )


def downgrade():
    op.drop_index(
        'idx_lessons_days_number_week_parity',
        table_name='lessons_days',
        schema=schema,
    )
    op.drop_table('lessons_days', schema=schema)
    WeekParitiesEnum.drop(op.get_bind(), checkfirst=True)
