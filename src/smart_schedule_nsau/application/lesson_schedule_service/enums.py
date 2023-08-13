from enum import StrEnum


class WeekParities(StrEnum):
    EVEN = 'четная'
    ODD = 'нечетная'


class LessonTypes(StrEnum):
    LECTURE = 'лекция'
    PRACTICAL = 'практика'
    LABORATORY = 'лабораторная'
