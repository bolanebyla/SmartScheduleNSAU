from enum import StrEnum

from telebot.types import KeyboardButton

from . import MAIN_MENU_KEYWORD
from .base import BaseKeyboard


class ScheduleButtons(StrEnum):
    CURRENT_WEEK = 'На текущую неделю'
    NEXT_WEEK = 'На следующую неделю'


class ScheduleKeyboard(BaseKeyboard):

    def add_buttons(self):
        btn1 = KeyboardButton(ScheduleButtons.CURRENT_WEEK)
        btn2 = KeyboardButton(ScheduleButtons.NEXT_WEEK)
        btn3 = KeyboardButton(MAIN_MENU_KEYWORD)

        self.add(btn1, btn2)
        self.add(btn3)
