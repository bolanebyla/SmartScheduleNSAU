# from sqlalchemy import Column, ForeignKey, Integer, String, Table

# from smart_schedule_nsau.adapters.database.meta import CASCADE, metadata

# study_groups = Table(
#     'study_groups',
#     lessons_schedule_metadata,
#     Column('name', String, primary_key=True),
#     Column(
#         'faculty_id',
#         ForeignKey('faculties.id', ondelete=CASCADE),
#         nullable=False
#     ),
#     Column('schedule_file_url', String, nullable=False),
#     Column('course', Integer, nullable=False),
# )
