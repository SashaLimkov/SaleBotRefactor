from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.settings.services.settings_user import get_settings
from bot.handlers.main.user_settings.currency import get_custom_currency_info
from bot.handlers.main.user_settings.formula import (
    get_formula_commission_text_and_selected_formula,
)
from bot.handlers.main.user_settings.logo_and_text_logo import (
    return_text_and_keyboard_for_wm_settings,
)
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw


async def main_settings_actions(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["second_lvl"])
    user_settings = get_settings(user_id)
    # user = get_profile_by_telegram_id(user_id)
    if user_action == 1:
        custom_cur = await get_custom_currency_info(telegram_id=user_id)
        selected_cur = "RUB" if user_settings.currency else "Валюта сайта"
        text = get_message_by_name_for_user(
            name="currency_settings_main", telegram_id=user_id
        ).text.format(custom_cur=custom_cur, selected_cur=selected_cur)
        keyboard = await ik.get_main_currency_settings_menu(callback_data=callback_data)
    elif user_action == 2:
        text, selected_formula = await get_formula_commission_text_and_selected_formula(
            user_id=user_id
        )
        keyboard = await ik.get_formula_commission(
            callback_data=callback_data, selected_formula=selected_formula
        )
    elif user_action == 3:
        selected_rounder = user_settings.rounder
        text = get_message_by_name_for_user(
            name="rounder_settings", telegram_id=user_id
        ).text.format(selected_rounder=selected_rounder)
        keyboard = await ik.get_rounder_settings_menu(callback_data=callback_data)
    elif user_action == 4:
        pass
    elif user_action == 5:
        text, keyboard = await return_text_and_keyboard_for_wm_settings(
            user_settings=user_settings, user_id=user_id, callback_data=callback_data
        )
    elif user_action == 6:
        text = get_message_by_name_for_user(
            name="product_settings", telegram_id=user_id
        ).text
        keyboard = await ik.get_product_settings_menu(
            callback_data=callback_data, telegram_id=user_id
        )
    elif user_action == 7:
        user_signature = user_settings.signature
        text_db = get_message_by_name_for_user(
            name="user_signature", telegram_id=user_id
        ).text
        text = (
            text_db.format(signature=user_signature)
            if user_signature
            else "Подпись отсутствует."
        )
        keyboard = await ik.get_signature_menu(
            callback_data=callback_data, user_signature=user_signature
        )
    elif user_action == 8:
        text = get_message_by_name_for_user(
            name="link_settings", telegram_id=user_id
        ).text
        keyboard = await ik.get_link_settings_menu(
            callback_data=callback_data, telegram_id=user_id
        )
    elif user_action == 9:
        text = get_message_by_name_for_user(
            name="channel_settings", telegram_id=user_id
        ).text
        keyboard = await ik.get_channels_menu(callback_data=callback_data)
    else:
        pass
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )
