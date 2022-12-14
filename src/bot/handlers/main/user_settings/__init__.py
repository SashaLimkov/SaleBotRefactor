from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from bot.data import callback_data as cd

from bot.handlers.main.user_settings import main_settings_menu, currency, rounder
from bot.states.Currency import Currency


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        main_settings_menu.main_settings_actions,
        cd.settings_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        currency.currency_settings,
        cd.settings_currency.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        currency.press_currency_to_update,
        cd.select_customize_currency.filter(),
        state="*"
    )
    dp.register_message_handler(
        currency.check_wrote_currency_value,
        state=Currency.GET_CUR_VALUE
    )
    dp.register_callback_query_handler(
        rounder.select_rounder_lvl,
        cd.settings_rounder.filter(),
        state="*"
    )
