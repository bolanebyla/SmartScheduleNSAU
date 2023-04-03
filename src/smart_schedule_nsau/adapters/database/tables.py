from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

CASCADE = 'CASCADE'

metadata = MetaData(naming_convention=naming_convention)

lesson_sequences = Table(
    'lesson_sequences',
    metadata,
    Column('number', Integer, primary_key=True),
    Column('start_time', DateTime, nullable=False),
    Column('end_time', DateTime, nullable=False),
)

# TODO: name - nullable=False
faculties = Table(
    'faculties',
    metadata,
    Column('id', String, primary_key=True),
    Column('name', String, nullable=True),
)

# study_groups = Table(
#     'study_groups',
#     metadata,
#     Column('name', String, primary_key=True),
#     Column('faculty_id', ForeignKey('faculties.id', ondelete=CASCADE),
#     nullable=False),
#     Column('schedule_file_url', String, nullable=False),
#     Column('course', Integer, nullable=False),
# )
