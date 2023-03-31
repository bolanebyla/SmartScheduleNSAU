from enum import Enum


class WeekParities(str, Enum):
    even = 'четная'
    odd = 'нечетная'


class LessonTypes(str, Enum):
    lecture = 'лекция'
    practical = 'практика'
    laboratory = 'лабораторная'
