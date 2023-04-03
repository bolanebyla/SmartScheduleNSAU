from sqlalchemy.orm import registry

from smart_schedule_nsau.application.lesson_schedule_service import entities

from . import tables

mapper = registry()

mapper.map_imperatively(entities.Faculty, tables.faculties)
