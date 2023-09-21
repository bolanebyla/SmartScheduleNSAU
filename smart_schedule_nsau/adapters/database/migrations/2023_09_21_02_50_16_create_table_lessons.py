"""Create table `lessons`

Revision ID: c147b0e00c4f
Revises: cfbe796b18c1
Create Date: 2023-09-21 02:50:16.040133+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c147b0e00c4f'
down_revision = 'cfbe796b18c1'
branch_labels = None
depends_on = None

metadata = sa.MetaData()
schema = 'lessons_schedule'

LessonTypesEnum = sa.Enum(
    'лекция',
    'практика',
    'лабораторная',
    values_callable=lambda x: [e.value for e in x],
    name='lesson_types',
    create_constraint=True,
    validate_strings=True,
    metadata=metadata,
    schema=schema,
)


def upgrade():
    LessonTypesEnum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'lessons',
        metadata,
        sa.Column('id', sa.Integer),
        sa.Column(
            'lessons_day_id',
            sa.Integer,
            nullable=False,
        ),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('time', sa.Time(timezone=True), nullable=False),
        sa.Column('teacher_full_name', sa.String, nullable=False),
        sa.Column('lesson_type', LessonTypesEnum, nullable=False),
        sa.Column('auditorium', sa.String, nullable=True),
        sa.Column('comment', sa.String, nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_lessons')),
        sa.ForeignKeyConstraint(
            ['lessons_day_id'],
            refcolumns=[f'{schema}.lessons_days.id'],
            name=op.f('fk_lessons_lessons_day_id_lessons_days'),
            ondelete='CASCADE',
        ),
        schema=schema,
    )
    op.create_index(
        'idx_lessons_name',
        'lessons',
        ['name'],
        schema=schema,
    )
    op.create_index(
        'idx_lessons_time',
        'lessons',
        ['time'],
        schema=schema,
    )


def downgrade():
    op.drop_index(
        'idx_lessons_name',
        table_name='lessons',
        schema=schema,
    )
    op.drop_index(
        'idx_lessons_time',
        table_name='lessons',
        schema=schema,
    )
    op.drop_table('lessons', schema=schema)
    LessonTypesEnum.drop(op.get_bind(), checkfirst=True)
