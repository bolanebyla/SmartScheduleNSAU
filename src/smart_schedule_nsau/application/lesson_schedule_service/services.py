from typing import List

from classic.components import component

from . import entities, interfaces


@component
class ScheduleCreator:

    async def recreate_schedule(
        self,
        uow: interfaces.IUnitOfWork,
        faculties: List[entities.Faculty],
    ):
        async with uow:
            await uow.schedule_change_repo.delete_schedule()
            uow.schedule_change_repo.create_schedule(faculties=faculties)

            await uow.commit()
