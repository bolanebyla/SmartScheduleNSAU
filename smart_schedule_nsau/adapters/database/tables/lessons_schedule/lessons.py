from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table, Time

from smart_schedule_nsau.adapters.database.meta import (
    CASCADE,
    lessons_schedule_schema,
    metadata,
)
from smart_schedule_nsau.application.lessons_schedule import LessonTypes

LessonTypesEnum = Enum(
    LessonTypes,
    values_callable=lambda x: [e.value for e in x],
    name='lesson_types',
    create_constraint=True,
    validate_strings=True,
    metadata=metadata,
    schema=lessons_schedule_schema,
)

# TODO: сделать мапинг на сущность

lessons = Table(
    'lessons',
    metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'lessons_day_id',
        Integer,
        ForeignKey('lessons_days.id', ondelete=CASCADE),
        nullable=False,
    ),
    Column('name', String, nullable=False, index=True),
    Column('time', Time(timezone=True), nullable=False, index=True),
    Column('teacher_full_name', String, nullable=False),
    Column('lesson_type', LessonTypesEnum, nullable=False),
    Column('auditorium', String, nullable=True),
    Column('comment', String, nullable=True),
    schema=lessons_schedule_schema,
)
