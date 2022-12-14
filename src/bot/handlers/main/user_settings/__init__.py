from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from bot.data import callback_data as cd

from bot.handlers.main.user_settings import main_settings_menu, currency, rounder, formula, product_settings
from bot.states.Commission import Commission
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
    dp.register_callback_query_handler(
        formula.formula_and_commission_menu,
        cd.settings_formula_and_comm.filter(),
        state="*"
    )
    dp.register_message_handler(
        formula.check_commission,
        state=Commission.GET_COMMISSION
    )
    dp.register_callback_query_handler(
        product_settings.product_settings_menu,
        cd.settings_product.filter(),
        state="*"
    )
