from aiogram import Dispatcher

from bot.data import callback_data as cd
from bot.handlers.main.subscriptions import buy_sub_or_add_helper, invoice, helper_sub, user_sub


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        buy_sub_or_add_helper.sub_or_add_helper_menu,
        cd.sub_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        user_sub.select_sub_to_buy,
        cd.rates_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        invoice.create_invoice_to_rate,
        cd.pay_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        helper_sub.buy_sub_to_helper,
        cd.rate_for_helper_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        helper_sub.success_sub_helper,
        cd.pay_menu_helper.filter(),
        state="*"
    )
