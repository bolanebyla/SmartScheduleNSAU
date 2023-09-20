from sqlalchemy import MetaData

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}
CASCADE = 'CASCADE'

lessons_schedule_schema = 'lessons_schedule'
lessons_schedule_metadata = MetaData(
    naming_convention=naming_convention,
    schema=lessons_schedule_schema,
)
