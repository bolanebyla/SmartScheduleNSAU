"""Create table `study_groups`

Revision ID: 28473bcc303b
Revises: c54ad3306e80
Create Date: 2023-04-04 03:10:52.670163+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '28473bcc303b'
down_revision = 'c54ad3306e80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'study_groups', sa.Column('name', sa.String(), nullable=False),
        sa.Column('faculty_id', sa.String(), nullable=False),
        sa.Column('schedule_file_url', sa.String(), nullable=False),
        sa.Column('course', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['faculty_id'], ['faculties.id'],
            name=op.f('fk_study_groups_faculty_id_faculties'),
            ondelete='CASCADE'
        ), sa.PrimaryKeyConstraint('name', name=op.f('pk_study_groups'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('study_groups')
    # ### end Alembic commands ###