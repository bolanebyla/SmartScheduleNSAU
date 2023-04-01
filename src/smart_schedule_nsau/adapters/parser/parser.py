import asyncio
import logging
import os
import uuid
from typing import Callable, List

import aiofiles
import aiofiles.os
import aiohttp
import xlrd
from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from classic.components import component

from smart_schedule_nsau.application.lesson_schedule_service import (
    Faculty,
    Lesson,
)

from ...application.lesson_schedule_service.enums import WeekParities
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

    async def save_schedule_file(self, file_response: ClientResponse) -> str:
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

        return schedule_file_path

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

    def parse_schedule_file(
        self, schedule_file: models.ScheduleFileInfo = None
    ) -> List[Lesson]:
        # if schedule_file.schedule_file_path is None:
        #     raise ValueError(
        #         'Field `schedule_file_path` is empty. '
        #         'Can not parse schedule from file'
        #     )

        lessons = []
        # schedule_file_path = schedule_file.schedule_file_path
        schedule_file_path = (
            'tmp/schedule_files\\'
            '56b5c973-531d-400a-ad5a-fb9a5e400118_ФВМ 1 курс.xls'
        )
        wb = xlrd.open_workbook(schedule_file_path)

        for sheet_name in wb.sheet_names():
            sh = wb.sheet_by_name(sheet_name)
            self.logger.debug(sh)
            schedule_rows = range(5, sh.nrows, 2)

            i = 0
            for rx in schedule_rows:

                if i == 0:
                    lesson_name = sh.row(rx)[1].value
                    print(lesson_name)
                    teacher_full_name = sh.row(rx)[40].value
                    print(teacher_full_name)

                #  максимальное число пар одного предмета за неделю
                max_week_lesson_sequence_number_count = 36

                lesson_sequence_number = 1
                for lessons_col_y in range(
                        4, max_week_lesson_sequence_number_count):
                    # получение аудитории
                    auditorium = str(sh.cell(rx, lessons_col_y).value).strip()

                    # получение сырых данных о группах у которых пара
                    groups_names_cell = sh.cell(rx + 1, lessons_col_y)
                    # если указано просто число
                    if groups_names_cell.ctype == xlrd.XL_CELL_NUMBER:
                        # то переводим в строку
                        groups_row_names = str(int(groups_names_cell.value))
                    else:
                        groups_row_names = str(groups_names_cell.value).strip()

                    # определение четности недели
                    if i == 0:
                        week_parity = WeekParities.odd
                    else:
                        week_parity = WeekParities.even

                    # определение дня недели
                    if lessons_col_y in list(range(4, 10)):
                        week_day_number = 1
                    elif lessons_col_y in list(range(10, 16)):
                        week_day_number = 2
                    elif lessons_col_y in list(range(16, 22)):
                        week_day_number = 3
                    elif lessons_col_y in list(range(22, 28)):
                        week_day_number = 4
                    elif lessons_col_y in list(range(28, 34)):
                        week_day_number = 5
                    elif lessons_col_y in list(range(34, 40)):
                        week_day_number = 6
                    else:
                        raise ValueError('Cant get `week_day_number`')

                    if groups_row_names:
                        print(
                            auditorium, groups_row_names, week_parity.value,
                            lesson_sequence_number, week_day_number
                        )

                    lesson_sequence_number += 1
                    if lesson_sequence_number == 7:
                        lesson_sequence_number = 1

                i += 1
                if i == 2:
                    i = 0

            break

        return lessons

    async def run_async(self):
        # schedule_files = await self.get_schedule_file_urls()
        # downloaded_schedule_files = await self.download_schedule_files(
        #     schedule_files=[schedule_files[6]],  # TODO: убрать индекс
        # )
        #
        # self.logger.debug(
        #     'downloaded_schedule_files: %s',
        #     downloaded_schedule_files
        # )

        # for schedule_file in downloaded_schedule_files:
        # schedule_file=schedule_file,
        await asyncio.to_thread(self.parse_schedule_file, )

        # self.logger.debug(downloaded_schedule_files)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_async())
