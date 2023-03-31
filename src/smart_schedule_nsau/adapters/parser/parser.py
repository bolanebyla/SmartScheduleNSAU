import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup
from classic.components import component


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

    async def parse_schedule(self):
        """
        Парсит страницу с расписанием
        """
        self.logger.debug('Получение html страницы с расписанием...')
        site_content = await self.get_schedule_site_content()

        self.logger.debug('Парсинг html страницы с расписанием...')
        faculties_groups = site_content.find_all(
            'div', class_='faculties_groups'
        )

        for faculty in faculties_groups:
            faculty_name = faculty.find('h2').text.strip()

            self.logger.debug('Факультет: %s', faculty_name)

            table = faculty.find('table')
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                course = row.find('th').text.strip()
                self.logger.debug('Курс %s', course)
                groups = row.find_all('td')

                for group in groups:
                    group_info = group.text.strip()
                    if not group_info:
                        continue

                    group_schedule_file_url = group.find('a').get('href')

                    self.logger.debug(
                        '%s (file url: %s)',
                        group_info,
                        group_schedule_file_url,
                    )

            self.logger.debug(faculty_name)

    async def run_async(self):
        await self.parse_schedule()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_async())
        loop.close()
