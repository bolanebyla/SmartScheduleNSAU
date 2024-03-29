import asyncio
import logging
import os
import uuid
from pprint import pprint
from typing import Callable, Dict, List

import aiofiles
import aiofiles.os
import aiohttp
import xlrd
from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from classic.components import component

from smart_schedule_nsau.application.lessons_schedule import (
    Faculty,
    Lesson,
    LessonTypes,
    ScheduleCreator,
    StudyGroup,
    WeekParities,
)

from ..database.uow import UnitOfWorkFactory
from . import models


@component
class ScheduleFileParser:

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def _create_group_name(self, group_prefix: str, group_number: int):
        """
        Создает название группы по префиксу и номеру
        """
        if len(str(group_number)) == 1:
            group_number = f'0{group_number}'

        group_name = f'{group_prefix}{group_number}'

        return group_name

    def _greate_groups(
        self, sheet_name: str, schedule_file: models.ScheduleFileInfo
    ) -> Dict[int, StudyGroup]:
        """
        Создает группы из названия листа
        """

        group_prefix = sheet_name[:2]
        groups_range_info = sheet_name[2:]

        # словарь с группами, чтобы распределять пары по группам
        groups_by_numbers: Dict[int, StudyGroup] = {}

        # если в названии есть "-", значит указан диапазон групп
        if '-' in groups_range_info:
            start_group_number, end_group_number = groups_range_info.split('-')

            for group_number in range(int(start_group_number),
                                      int(end_group_number) + 1):
                group_name = self._create_group_name(
                    group_prefix=group_prefix,
                    group_number=group_number,
                )

                groups_by_numbers[group_number] = StudyGroup(
                    name=group_name,
                    schedule_file_url=schedule_file.schedule_file_url,
                    course=schedule_file.course,
                )

        # если нет, то лист для одной группы
        else:
            group_number = int(groups_range_info)
            group_name = self._create_group_name(
                group_prefix=group_prefix,
                group_number=group_number,
            )
            groups_by_numbers[group_number] = StudyGroup(
                name=group_name,
                schedule_file_url=schedule_file.schedule_file_url,
                course=schedule_file.course,
            )

        return groups_by_numbers

    def parse_schedule_file(
        self,
        schedule_file: models.ScheduleFileInfo = None
    ) -> List[StudyGroup]:
        if schedule_file.schedule_file_path is None:
            raise ValueError(
                'Field `schedule_file_path` is empty. '
                'Can not parse schedule from file'
            )

        # schedule_file = models.ScheduleFileInfo(
        #     course=1,
        #     schedule_file_url='test',
        #     schedule_file_path=(
        #         'tmp/schedule_files\\'
        #         '56b5c973-531d-400a-ad5a-fb9a5e400118_ФВМ 1 курс.xls'
        #     )
        # )

        schedule_file_path = schedule_file.schedule_file_path

        wb = xlrd.open_workbook(schedule_file_path)

        groups = []
        for sheet_name in wb.sheet_names():
            if sheet_name == 'Выписки':
                continue

            sh = wb.sheet_by_name(sheet_name)
            self.logger.debug(sh)
            schedule_rows = range(5, sh.nrows, 2)

            # создаем группы
            groups_by_numbers = self._greate_groups(
                sheet_name=sheet_name,
                schedule_file=schedule_file,
            )
            print(groups_by_numbers)
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
                    # получение аудиторий
                    audiences = str(sh.cell(rx, lessons_col_y).value
                                    ).strip().split(' ')

                    # получение сырых данных о группах у которых пара
                    groups_names_cell = sh.cell(rx + 1, lessons_col_y)
                    # если указано просто число
                    if groups_names_cell.ctype == xlrd.XL_CELL_NUMBER:
                        # то переводим в строку
                        groups_row_names = str(int(groups_names_cell.value)
                                               ).strip().split(',')
                    else:
                        groups_row_names = str(groups_names_cell.value
                                               ).strip().split(',')

                    # определение четности недели
                    if i == 0:
                        week_parity = WeekParities.ODD
                    else:
                        week_parity = WeekParities.EVEN

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

                    if groups_row_names and lesson_name:
                        # TODO: вынести в отдельный метод
                        try:
                            for groups_row_name, auditorium in zip(
                                    groups_row_names, audiences):

                                if groups_row_name.lower() == 'л':
                                    lesson_type = LessonTypes.LECTURE
                                else:
                                    lesson_type = LessonTypes.PRACTICAL

                                lesson = Lesson(
                                    name=lesson_name,
                                    week_day_number=week_day_number,
                                    sequence_number=lesson_sequence_number,
                                    week_parity=week_parity,
                                    teacher_full_name=teacher_full_name,
                                    lesson_type=lesson_type,
                                    auditorium=auditorium,
                                )

                                # если указана лекция,
                                # то добавляем ко всем группам
                                if lesson_type == LessonTypes.LECTURE:
                                    for group in groups_by_numbers.values():
                                        group.lessons.append(lesson)
                                # если указан только номер группы, то к ней
                                elif groups_row_name.isdigit():
                                    group_number = int(groups_row_name)
                                    groups_by_numbers[group_number
                                                      ].lessons.append(lesson)
                                # если указана подгруппа,
                                # то добавляем к группе с указанием подгруппы
                                elif groups_row_name[-1].isalpha():
                                    group_number = int(groups_row_name[:-1])
                                    subgroup = groups_row_name[-1]
                                    lesson.subgroup = subgroup
                                    groups_by_numbers[group_number
                                                      ].lessons.append(lesson)

                        except Exception as e:
                            self.logger.warning(e)

                    lesson_sequence_number += 1
                    if lesson_sequence_number == 7:
                        lesson_sequence_number = 1

                i += 1
                if i == 2:
                    i = 0

            groups.extend(groups_by_numbers.values())

            break
        pprint(groups)
        return groups


@component
class ScheduleSiteParser:
    """
    Парсер расписания с сайта и excel файлов
    """
    schedule_url: str
    chunk_size_bytes: int
    uuid_gen: Callable = uuid.uuid4

    schedule_file_parser: ScheduleFileParser

    max_save_schedule_files_workers: int = 10
    save_schedule_files_dir: str

    uow_factory: UnitOfWorkFactory

    schedule_creator: ScheduleCreator

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

    async def get_schedule_file_urls(self) -> List[models.ParsedData]:
        """
        Получает ссылки на файлы с расписанием с сайта
        """
        self.logger.debug('Получение html страницы с расписанием...')
        site_content = await self.get_schedule_site_content()

        self.logger.debug('Парсинг html страницы с расписанием...')
        faculties_groups_data = site_content.find_all(
            'div', class_='faculties_groups'
        )

        parsed_data = []
        for faculty_data in faculties_groups_data:
            faculty_name = faculty_data.find('h2').text.strip()

            faculty = Faculty(name=faculty_name)
            data = models.ParsedData(faculty=faculty, )

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

                    data.schedule_files.append(
                        models.ScheduleFileInfo(
                            course=course_number,
                            schedule_file_url=group_schedule_file_url,
                        )
                    )

        return parsed_data

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

        parsed_data = [
            models.ParsedData(
                faculty=Faculty(
                    id='test',
                    name='test',
                    study_groups=[],
                ),
                schedule_files=[
                    models.ScheduleFileInfo(
                        course=1,
                        schedule_file_url='test',
                        schedule_file_path=(
                            'tmp/schedule_files\\'
                            '56b5c973-531d-400a-ad5a-fb9a5e400118_ФВМ '
                            '1 курс.xls'
                        )
                    )
                ]
            )
        ]

        faculties = []
        for data in parsed_data:
            for schedule_file in data.schedule_files:
                groups = await asyncio.to_thread(
                    self.schedule_file_parser.parse_schedule_file,
                    schedule_file=schedule_file,
                )
                data.faculty.study_groups.extend(groups)

            faculties.append(data.faculty)

        # for schedule_file in downloaded_schedule_files:
        # schedule_file=schedule_file,

        await self.schedule_creator.recreate_schedule(
            uow=self.uow_factory.create_uow(),
            faculties=faculties,
        )

        # self.logger.debug(downloaded_schedule_files)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_async())
