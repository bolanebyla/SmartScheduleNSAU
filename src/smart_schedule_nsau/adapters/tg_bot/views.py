from abc import ABC, abstractmethod
from datetime import datetime

from smart_schedule_nsau.application.lesson_schedule_service import (
    Lesson,
    LessonsDay,
)

# разделитель между занятиями (парами) при отображении
LESSONS_SEPARATOR = '-' * 43


def _is_it_today(lessons_day: LessonsDay) -> bool:
    """
    Проверяет проходит ли переданный учебный день сегодня
    :param lessons_day: учебный день
    :return: True - проходит сегодня
    """
    # TODO: учитывать таймзону
    date_now = datetime.now()
    return date_now.weekday() + 1 == lessons_day.number


class BaseMessageTextView(ABC):
    """
    Базовый класс представлений для отображения в сообщениях чат бота
    """

    @abstractmethod
    def to_str(self) -> str:
        ...

    def __str__(self):
        return self.to_str()


class LessonView(BaseMessageTextView):
    """
    Представление занятия (пары) в формате для отображения
    """

    def __init__(self, lesson: Lesson):
        self._lesson = lesson

    def to_str(self) -> str:
        auditorium = (
            f'Аудитория: {self._lesson.auditorium}\n'
            if self._lesson.auditorium else ''
        )
        comment = (
            f'\nПримечание: {self._lesson.comment}'
            if self._lesson.comment else ''
        )
        lessons_str = f'{self._lesson.time.strftime("%H:%M")}\n' \
                      f'{auditorium}' \
                      f'👉{self._lesson.name}\n' \
                      f'({self._lesson.lesson_type}) ' \
                      f'{self._lesson.teacher_full_name}' \
                      f'{comment}'

        return lessons_str


class LessonsDayView(BaseMessageTextView):
    """
    Представление занятий (пар) одного дня в формате для отображения
    """

    def __init__(self, lessons_day: LessonsDay):
        self._lessons_day = lessons_day

    def to_str(self) -> str:
        # день недели
        if _is_it_today(self._lessons_day):
            lessons_view_str = f'🍏{self._lessons_day.name.upper()}🍏'
        else:
            lessons_view_str = f'🍎{self._lessons_day.name.upper()}🍎'

        lessons_view_str += f'\n{LESSONS_SEPARATOR}\n'

        # занятия (пары)
        for lessons in self._lessons_day.lessons:
            lesson_view = LessonView(lesson=lessons)
            lesson_view_str = lesson_view.to_str()

            lessons_view_str += lesson_view_str
            lessons_view_str += f'\n{LESSONS_SEPARATOR}\n'

        return lessons_view_str
