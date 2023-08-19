from sqlalchemy.orm import registry

# from smart_schedule_nsau.application.lessons_schedule import entities
#
# from . import tables

mapper = registry()
#
# mapper.map_imperatively(entities.LessonSequence, tables.lesson_sequences)
#
# mapper.map_imperatively(
#     entities.Lesson,
#     tables.lessons,
#     # properties={
#     #     'sequence': relationship(
#     #         entities.LessonSequence,
#     #         uselist=False,
#     #         lazy='joined',
#     #     )
#     # }
# )
#
# mapper.map_imperatively(
#     entities.StudyGroup,
#     tables.study_groups,
#     properties={
#         'lessons': relationship(
#             entities.Lesson, lazy='subquery', cascade='all, delete-orphan'
#         )
#     }
# )
#
# mapper.map_imperatively(
#     entities.Faculty,
#     tables.faculties,
#     properties={
#         'study_groups': relationship(
#             entities.StudyGroup, lazy='subquery', cascade='all, delete-orphan'
#         )
#     }
# )
