from enum import StrEnum

from telebot.types import KeyboardButton

from .base import BaseKeyboard


class MainMenuButtons(StrEnum):
    SCHEDULE = 'Расписание 🗓'
    NEAREST_LESSON = 'Ближайшая пара ⏱'
    SCHEDULE_FOR_TODAY = 'Расписание на сегодня 🍏'
    SCHEDULE_FOR_TOMORROW = 'Расписание на завтра 🍎'
    SEARCH = 'Поиск 🔎'
    MORE_INFO = 'Другое ⚡'


class MainMenuKeyboard(BaseKeyboard):

    def add_buttons(self):
        btn1 = KeyboardButton(MainMenuButtons.SCHEDULE)
        btn2 = KeyboardButton(MainMenuButtons.NEAREST_LESSON)
        btn3 = KeyboardButton(MainMenuButtons.SCHEDULE_FOR_TODAY)
        btn4 = KeyboardButton(MainMenuButtons.SCHEDULE_FOR_TOMORROW)
        btn5 = KeyboardButton(MainMenuButtons.SEARCH)
        btn6 = KeyboardButton(MainMenuButtons.MORE_INFO)

        self.add(btn1, btn2)
        self.add(btn3)
        self.add(btn4)
        self.add(btn5, btn6)
