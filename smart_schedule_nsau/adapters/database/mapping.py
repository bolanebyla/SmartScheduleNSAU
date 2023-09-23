from sqlalchemy.orm import registry, relationship

from smart_schedule_nsau.application.lessons_schedule import Lesson, LessonsDay

from .tables import lessons, lessons_days

mapper = registry()

mapper.map_imperatively(Lesson, lessons)

mapper.map_imperatively(
    LessonsDay,
    lessons_days,
    properties={
        'lessons': relationship(
            Lesson, lazy='subquery', cascade='all, delete-orphan'
        )
    }
)
