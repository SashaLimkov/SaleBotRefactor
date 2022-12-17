from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.data import callback_data as cd
from bot.handlers.main.posts import date_and_inline


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        date_and_inline.show_compilations_by_date_call,
        cd.select_date.filter(),
        state="*"
    )
    dp.register_inline_handler(
        date_and_inline.inline_compilations,
        state="*"
    )
    dp.register_message_handler(
        date_and_inline.sender_anons,
        filters.Text(contains="|:|"),
        state="*"
    )
