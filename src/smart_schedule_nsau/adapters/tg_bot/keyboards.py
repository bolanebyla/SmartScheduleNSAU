from abc import ABC, abstractmethod

from telebot.types import KeyboardButton, ReplyKeyboardMarkup


class BaseKeyboard(ReplyKeyboardMarkup, ABC):

    def __init__(self):
        super().__init__(one_time_keyboard=False, resize_keyboard=True)
        self.add_buttons()

    @abstractmethod
    def add_buttons(self):
        ...


class MainMenuKeyboard(BaseKeyboard):

    def add_buttons(self):
        btn1 = KeyboardButton('Расписание 🗓')
        btn2 = KeyboardButton('Ближайшая пара ⏱')
        btn3 = KeyboardButton('Расписание на сегодня 🍏')
        btn4 = KeyboardButton('Расписание на завтра 🍎')
        btn5 = KeyboardButton('Поиск 🔎')
        btn6 = KeyboardButton('Другое ⚡')

        self.add(btn1, btn2)
        self.add(btn3)
        self.add(btn4)
        self.add(btn5, btn6)
