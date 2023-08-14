from abc import ABC, abstractmethod

from smart_schedule_nsau.application.lesson_schedule_service import Lesson
from smart_schedule_nsau.application.lesson_schedule_service.entities import (
    LessonsDay,
)

LESSONS_SEPARATOR = '-' * 43


class BaseView(ABC):

    @abstractmethod
    def to_str(self) -> str:
        ...

    def __str__(self):
        return self.to_str()


class LessonView(BaseView):
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


class LessonsDayView(BaseView):
    """
    Представление занятий (пар) одного дня в формате для отображения
    """

    def __init__(self, lessons_day: LessonsDay):
        self._lessons_day = lessons_day

    def to_str(self) -> str:
        lessons_view_str = f'{self._lessons_day.name.upper()}\n'
        for lessons in self._lessons_day.lessons:
            lesson_view = LessonView(lesson=lessons)
            lesson_view_str = lesson_view.to_str()

            lessons_view_str += lesson_view_str
            lessons_view_str += f'\n{LESSONS_SEPARATOR}\n'

        return lessons_view_str
