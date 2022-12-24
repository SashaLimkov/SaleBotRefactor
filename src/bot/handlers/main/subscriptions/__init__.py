from aiogram import Dispatcher
from aiogram.types import ContentType

from bot.data import callback_data as cd
from bot.filters import IsTrial, IsHelper, IsEndedSub
from bot.handlers.main.subscriptions import buy_sub_or_add_helper, invoice, helper_sub, user_sub, add_helper, ended_sub


def setup(dp: Dispatcher):
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
        invoice.create_invoice_to_rate,
        cd.pay_menu_helper.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        helper_sub.buy_sub_to_helper,
        cd.rate_for_helper_menu.filter(),
        state="*"
    )
    dp.register_pre_checkout_query_handler(invoice.check_payment, state='*')
    dp.register_message_handler(invoice.oplata_ok, content_types=ContentType.SUCCESSFUL_PAYMENT, state='*')

    dp.register_callback_query_handler(
        buy_sub_or_add_helper.sub_or_add_helper_menu,
        cd.sub_menu_ended.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        ended_sub.sub_ended,
        IsEndedSub(),
        state="*"
    )
    dp.register_callback_query_handler(
        add_helper.not_allowed_at_trial,
        IsTrial(),
        cd.sub_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        add_helper.not_allowed_helper,
        IsHelper(),
        cd.sub_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        buy_sub_or_add_helper.sub_or_add_helper_menu,
        cd.sub_menu.filter(),
        state="*"
    )
