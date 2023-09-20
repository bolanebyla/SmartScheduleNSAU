from sqlalchemy import Column, ForeignKey, Integer, String, Table

# TODO: убрать зависимость от postgresql
from sqlalchemy.dialects.postgresql import ENUM

from smart_schedule_nsau.adapters.database.meta import (
    CASCADE,
    lessons_schedule_metadata,
)
from smart_schedule_nsau.application.lessons_schedule import (
    LessonTypes,
    WeekParities,
)

WEEK_PARITIES_ENUM = ENUM(
    WeekParities,
    name='week_parities',
    metadata=lessons_schedule_metadata,
    create_type=False,
    validate_strings=True,
)

LESSON_TYPES_ENUM = ENUM(
    LessonTypes,
    name='lesson_types',
    metadata=lessons_schedule_metadata,
    create_type=False,
    validate_strings=True,
)

# TODO: добавить primary_key
lessons = Table(
    'lessons',
    lessons_schedule_metadata,
    Column('name', String),
    Column('week_day_number', Integer),
    Column('sequence_number', Integer, nullable=False),
    Column('week_parity', WEEK_PARITIES_ENUM),
    Column('teacher_full_name', String),
    Column('lesson_type', LESSON_TYPES_ENUM),
    Column('auditorium', String),
    Column(
        'study_group_name',
        ForeignKey('study_groups.name', ondelete=CASCADE),
        nullable=False
    ),
    Column('subgroup', String, nullable=True),
)
