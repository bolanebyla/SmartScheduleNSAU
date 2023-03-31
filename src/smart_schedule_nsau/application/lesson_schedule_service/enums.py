from enum import Enum


class WeekParities(Enum, str):
    even = 'четная'
    odd = 'нечетная'


class LessonTypes(Enum, str):
    lecture = 'лекция'
    practical = 'практика'
    laboratory = 'лабораторная'
