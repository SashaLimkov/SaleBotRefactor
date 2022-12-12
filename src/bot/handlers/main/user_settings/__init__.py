from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from bot.data import callback_data as cd

from bot.handlers.main.user_settings import main_settings_menu


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        main_settings_menu.main_settings_actions,
        cd.settings_menu.filter(),
        state="*"
    )
