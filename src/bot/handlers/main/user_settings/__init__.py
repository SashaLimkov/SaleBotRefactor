from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from bot.data import callback_data as cd

from bot.handlers.main.user_settings import (
    main_settings_menu,
    currency,
    rounder,
    formula,
    product_settings,
    user_signature,
    link_settings,
    user_channels,
    logo_and_text_logo,
)
from bot.states.Commission import Commission
from bot.states.Currency import Currency
from bot.states.LogoAndTLogo import LogoAndTLogo
from bot.states.Signature import Signature


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        main_settings_menu.main_settings_actions, cd.settings_menu.filter(), state="*"
    )
    dp.register_callback_query_handler(
        currency.currency_settings, cd.settings_currency.filter(), state="*"
    )
    dp.register_callback_query_handler(
        currency.press_currency_to_update,
        cd.select_customize_currency.filter(),
        state="*",
    )
    dp.register_message_handler(
        currency.check_wrote_currency_value, state=Currency.GET_CUR_VALUE
    )
    dp.register_callback_query_handler(
        rounder.select_rounder_lvl, cd.settings_rounder.filter(), state="*"
    )
    dp.register_callback_query_handler(
        formula.formula_and_commission_menu,
        cd.settings_formula_and_comm.filter(),
        state="*",
    )
    dp.register_message_handler(
        formula.check_commission, state=Commission.GET_COMMISSION
    )
    dp.register_callback_query_handler(
        product_settings.product_settings_menu, cd.settings_product.filter(), state="*"
    )
    dp.register_callback_query_handler(
        user_signature.user_signature_menu, cd.settings_signature.filter(), state="*"
    )
    dp.register_message_handler(
        user_signature.set_user_signature, state=Signature.GET_SIGNATURE
    )
    dp.register_callback_query_handler(
        link_settings.link_settings_menu, cd.settings_link.filter(), state="*"
    )
    dp.register_callback_query_handler(
        user_channels.get_tg_channels_and_instructions,
        cd.settings_channel.filter(),
        state="*",
    )
    dp.register_callback_query_handler(
        logo_and_text_logo.logo_and_t_logo_settings, cd.settings_wm.filter(), state="*"
    )
    dp.register_message_handler(
        logo_and_text_logo.set_t_logo,
        content_types=types.ContentTypes.ANY,
        state=LogoAndTLogo.EDIT_TEXT_LOGO
    )
    dp.register_message_handler(
        logo_and_text_logo.set_logo,
        content_types=types.ContentTypes.ANY,
        state=LogoAndTLogo.EDIT_LOGO
    )
    dp.register_callback_query_handler(
        logo_and_text_logo.set_logo_or_t_logo_position,
        cd.settings_wm_position.filter(),
        state="*",
    )
