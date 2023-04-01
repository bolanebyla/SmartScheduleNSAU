import asyncio
import logging
import os
import uuid
from typing import Callable, List

import aiofiles
import aiofiles.os
import aiohttp
from aiohttp import ClientResponse
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
    chunk_size_bytes: int
    uuid_gen: Callable = uuid.uuid4

    max_save_schedule_files_workers: int = 10
    save_schedule_files_dir: str

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
        Получает ссылки на файлы с расписанием с сайта
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

    async def save_schedule_file(self, file_response: ClientResponse):
        """
        Сохраняет файл с расписанием на диск
        """
        original_filename = file_response.content_disposition.filename
        schedule_file_name = f'{self.uuid_gen()}_{original_filename}'

        await aiofiles.os.makedirs(self.save_schedule_files_dir, exist_ok=True)

        schedule_file_path = os.path.join(
            self.save_schedule_files_dir,
            schedule_file_name,
        )

        async with aiofiles.open(schedule_file_path, 'wb') as f:
            while True:
                chunk = await file_response.content.read(self.chunk_size_bytes)
                if not chunk:
                    break
                await f.write(chunk)

    async def download_schedule_file(
        self,
        schedule_file_info: models.ScheduleFileInfo,
        semaphore: asyncio.BoundedSemaphore,
    ) -> models.ScheduleFileInfo:
        """
        Загружает файл с расписанием
        """

        self.logger.debug(schedule_file_info)

        file_url = schedule_file_info.schedule_file_url

        async with aiohttp.ClientSession() as session:
            # получаем файл
            async with session.get(file_url) as resp:
                async with semaphore:
                    # сохраняем файл
                    schedule_file_path = await self.save_schedule_file(
                        file_response=resp,
                    )

        schedule_file_info.schedule_file_path = schedule_file_path

        self.logger.debug('"%s" downloaded', file_url)

        return schedule_file_info

    async def download_schedule_files(
        self, schedule_files: List[models.ScheduleFileInfo]
    ) -> List[models.ScheduleFileInfo]:

        semaphore = asyncio.BoundedSemaphore(
            self.max_save_schedule_files_workers
        )

        parse_tasks = [
            asyncio.ensure_future(
                self.download_schedule_file(file_info, semaphore)
            ) for file_info in schedule_files
        ]

        downloaded_schedule_files = await asyncio.gather(*parse_tasks)

        return downloaded_schedule_files

    async def parse_schedule_file(
        self, schedule_file: models.ScheduleFileInfo
    ) -> List[Lesson]:
        lessons = []

        return lessons

    async def run_async(self):
        schedule_files = await self.get_schedule_file_urls()
        self.logger.debug('schedule_files_info %s', schedule_files)

        downloaded_schedule_files = await self.download_schedule_files(
            schedule_files=schedule_files
        )

        self.logger.debug(downloaded_schedule_files)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_async())
