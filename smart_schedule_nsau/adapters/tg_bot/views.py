from abc import ABC, abstractmethod

from smart_schedule_nsau.application.lessons_schedule import Lesson, LessonsDay

# разделитель между занятиями (парами) при отображении
LESSONS_SEPARATOR = '-' * 43


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

    def __init__(self, lessons_day: LessonsDay, mark_as_today: bool = False):
        self._lessons_day = lessons_day
        self._mark_as_today = mark_as_today

    def to_str(self) -> str:
        # день недели
        if self._mark_as_today:
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
