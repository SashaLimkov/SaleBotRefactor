from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_by_telegram_id
from apps.profiles.services.subscription import get_user_active_subscription
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw


async def main_settings_actions(
        call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["second_lvl"])
    # user = get_profile_by_telegram_id(user_id)
    if user_action == 1:
        custom_cur = ""
        selected_cur = ""
        text = get_message_by_name_for_user(name="currency_settings_main", telegram_id=user_id).text.format(
            custom_cur=custom_cur,
            selected_cur=selected_cur
        )
        keyboard = await ik.get_main_currency_settings_menu(callback_data=callback_data)
    elif user_action == 2:
        pass
    elif user_action == 3:
        selected_rounder = 1
        text = get_message_by_name_for_user(name="rounder_settings", telegram_id=user_id).text.format(
            selected_rounder=selected_rounder)
        keyboard = await ik.get_rounder_settings_menu(callback_data=callback_data)
    elif user_action == 4:
        pass
    elif user_action == 5:
        pass
    elif user_action == 6:
        pass
    elif user_action == 7:
        pass
    elif user_action == 8:
        pass
    elif user_action == 9:
        pass
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
