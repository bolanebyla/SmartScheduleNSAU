from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


class ScheduleHandlers:

    async def show_current_week_schedule(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает расписание на текущую неделю
        """

        group_name = '123-1'
        week_parity_name = 'четная'

        schedule_info_text = f'Расписание {group_name}\n' \
                             f'Неделя: {week_parity_name}'

        # TODO: вынести формирование расписания в отдельный метод
        schedule_for_day_1 = '''
        🍎ПОНЕДЕЛЬНИК🍎
-------------------------------------------
11:45
Аудитория: Ж-321
👉Технология построения защищенных компьютерных сетей
( Лекция ) Бжевский Кирилл Петрович
-------------------------------------------
13:45
Аудитория: Ж-309
👉Основы управления информационной безопасностью
( Практ. ) Маринов Александр Андреевич
-------------------------------------------
        '''
        schedule_for_day_2 = '''
        🍎ВТОРНИК🍎
-------------------------------------------
11:45
Аудитория: Ж-309
👉Безопасность систем баз данных
( Лекция ) Тюрнев Александр Сергеевич
-------------------------------------------
13:45
Аудитория: Ж-309
👉Основы управления информационной безопасностью
( Лекция ) Маринов Александр Андреевич
-------------------------------------------
15:30
Аудитория: Ж-309
👉Безопасность систем баз данных
( Лаб. раб. подгруппа 2 ) Тюрнев Александр Сергеевич
-------------------------------------------'''

        schedule_text_by_days = [schedule_for_day_1, schedule_for_day_2]

        await bot.send_message(
            chat_id=message.chat.id,
            text=schedule_info_text,
        )

        for schedule_for_day in schedule_text_by_days:
            await bot.send_message(
                chat_id=message.chat.id,
                text=schedule_for_day,
            )
