import asyncio
import logging
from typing import List

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from classic.components import component

from smart_schedule_nsau.application.lesson_schedule_service import (
    Faculty,
    Lesson,
)

from . import models


@component
class ScheduleParser:
    """
    Парсер расписания с сайта и excel файлов
    """
    schedule_url: str

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def get_schedule_site_content(self) -> BeautifulSoup:
        """
        Получает html страницу с расписанием
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.schedule_url) as resp:
                text = await resp.read()

        result = BeautifulSoup(text, features='html.parser')
        return result

    async def get_schedule_file_urls(self) -> List[models.ScheduleFileInfo]:
        """
        Парсит страницу с расписанием
        """
        self.logger.debug('Получение html страницы с расписанием...')
        site_content = await self.get_schedule_site_content()

        self.logger.debug('Парсинг html страницы с расписанием...')
        faculties_groups_data = site_content.find_all(
            'div', class_='faculties_groups'
        )

        schedule_files = []
        for faculty_data in faculties_groups_data:
            faculty_name = faculty_data.find('h2').text.strip()

            faculty = Faculty(name=faculty_name)

            table_data = faculty_data.find('table')
            table_body_data = table_data.find('tbody')

            rows_data = table_body_data.find_all('tr')
            for row_data in rows_data:
                course_number = row_data.find('th').text.strip()

                groups_data = row_data.find_all('td')

                for group_data in groups_data:
                    group_info = group_data.text.strip()
                    if not group_info:
                        continue

                    group_schedule_file_url = group_data.find('a').get('href')

                    schedule_files.append(
                        models.ScheduleFileInfo(
                            course=course_number,
                            schedule_file_url=group_schedule_file_url,
                            faculty=faculty,
                        )
                    )

        return schedule_files

    async def parse_schedule_from_file(
        self,
        schedule_file_info: models.ScheduleFileInfo,
    ) -> Lesson:
        self.logger.debug(schedule_file_info)

        file_url = schedule_file_info.schedule_file_url

        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:

                content = await resp.content.read()

                schedule_file_name = f'{file_url[-5:-1]}_test.xls'

                async with aiofiles.open(f'tmp/{schedule_file_name}',
                                         'wb') as f:
                    await f.write(content)

    async def parse_schedule_from_files(
        self, schedule_files: List[models.ScheduleFileInfo]
    ):

        parse_tasks = [
            self.parse_schedule_from_file(file_info)
            for file_info in schedule_files
        ]

        result = await asyncio.gather(*parse_tasks)
        self.logger.debug(result)

    async def run_async(self):
        schedule_files = await self.get_schedule_file_urls()
        self.logger.debug('schedule_files_info %s', schedule_files)

        await self.parse_schedule_from_files(schedule_files=schedule_files)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_async())
