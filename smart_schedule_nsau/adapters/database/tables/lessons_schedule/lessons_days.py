from sqlalchemy import Column, Enum, Index, Integer, Table

from smart_schedule_nsau.adapters.database.meta import (
    lessons_schedule_schema,
    metadata,
)
from smart_schedule_nsau.application.lessons_schedule import WeekParities

WeekParitiesEnum = Enum(
    WeekParities,
    values_callable=lambda x: [e.value for e in x],
    name='week_parities',
    create_constraint=True,
    validate_strings=True,
    metadata=metadata,
    schema=lessons_schedule_schema,
)

lessons_days = Table(
    'lessons_days',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('number', Integer, nullable=False),
    Column('week_parity', WeekParitiesEnum, nullable=False),
    Index('idx_lessons_days_number_week_parity', 'number', 'week_parity'),
    schema=lessons_schedule_schema,
)
