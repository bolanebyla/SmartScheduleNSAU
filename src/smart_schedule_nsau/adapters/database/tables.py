from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Time,
)
from sqlalchemy.dialects.postgresql import ENUM

from smart_schedule_nsau.application.lesson_schedule_service import (
    LessonTypes,
    WeekParities,
)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

CASCADE = 'CASCADE'

metadata = MetaData(naming_convention=naming_convention)

# TODO: name - nullable=False
faculties = Table(
    'faculties',
    metadata,
    Column('id', String, primary_key=True),
    Column('name', String, nullable=True),
)

study_groups = Table(
    'study_groups',
    metadata,
    Column('name', String, primary_key=True),
    Column(
        'faculty_id',
        ForeignKey('faculties.id', ondelete=CASCADE),
        nullable=False
    ),
    Column('schedule_file_url', String, nullable=False),
    Column('course', Integer, nullable=False),
)

lesson_sequences = Table(
    'lesson_sequences',
    metadata,
    Column('number', Integer, primary_key=True),
    Column('start_time', Time, nullable=False),
    Column('end_time', Time, nullable=False),
)

WEEK_PARITIES_ENUM = ENUM(
    WeekParities,
    name='week_parities',
    metadata=metadata,
    create_type=False,
    validate_strings=True,
)

LESSON_TYPES_ENUM = ENUM(
    LessonTypes,
    name='lesson_types',
    metadata=metadata,
    create_type=False,
    validate_strings=True,
)

lessons = Table(
    'lessons',
    metadata,
    Column('name', String, primary_key=True),
    Column('week_day_number', Integer, primary_key=True),
    Column(
        'sequence_number',
        ForeignKey('lesson_sequences.number', ondelete=CASCADE),
        nullable=False
    ),
    Column('week_parity', WEEK_PARITIES_ENUM, primary_key=True),
    Column('teacher_full_name', String, primary_key=True),
    Column('lesson_type', LESSON_TYPES_ENUM, primary_key=True),
    Column('auditorium', String, primary_key=True),
    Column(
        'study_group_name',
        ForeignKey('study_groups.name', ondelete=CASCADE),
        nullable=False
    ),
    Column('subgroup', String, nullable=True),
)
