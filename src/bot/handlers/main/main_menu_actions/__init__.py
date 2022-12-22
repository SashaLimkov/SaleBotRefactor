from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.data import callback_data as cd
from bot.handlers.main.main_menu_actions import main_menu


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        main_menu.main_menu_actions, cd.mm.filter(), state="*"
    )
    dp.register_callback_query_handler(
        main_menu.get_main_menu, filters.Text(cd.MAIN_MENU), state="*"
    )
