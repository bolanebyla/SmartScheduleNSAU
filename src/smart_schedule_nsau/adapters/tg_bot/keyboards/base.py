from abc import ABC, abstractmethod

from telebot.types import ReplyKeyboardMarkup


class BaseKeyboard(ReplyKeyboardMarkup, ABC):

    def __init__(self):
        super().__init__(one_time_keyboard=False, resize_keyboard=True)
        self.add_buttons()

    @abstractmethod
    def add_buttons(self):
        ...
