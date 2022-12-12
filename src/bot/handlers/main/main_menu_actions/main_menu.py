from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_by_telegram_id
from apps.profiles.services.subscription import get_user_active_subscription
from bot.states.MainMenu import MainMenu
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik


async def get_main_menu(call: types.CallbackQuery, state: FSMContext):
    await MainMenu.MAIN_MENU.set()
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user = get_profile_by_telegram_id(telegram_id=user_id)
    text = get_message_by_name_for_user(name="confirm_registration", telegram_id=user_id).text.format(
        name=user.first_name)
    await mw.try_edit_message(
        user_id=user_id,
        text=text,
        message=call.message,
        state=state,
        main_message_id=main_message_id,
        keyboard=await ik.get_main_menu(user.in_chat)
    )


async def main_menu_actions(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["action"])
    user = get_profile_by_telegram_id(user_id)
    if user_action == 1:
        text = get_message_by_name_for_user(name="settings_menu", telegram_id=user_id).text
        keyboard = await ik.get_settings_menu(callback_data=callback_data)
    elif user_action == 2:
        text = get_message_by_name_for_user(name="select_date", telegram_id=user_id).text
        keyboard = await ik.get_date_menu()
    elif user_action == 3:
        sub = get_user_active_subscription(user_id)
        text = get_message_by_name_for_user(name="check_cub", telegram_id=user_id).text.format(sub_days=sub.days_left)
        keyboard = await ik.get_sub_menu(is_active=user.is_active, is_helper=user.is_helper,
                                         callback_data=callback_data)
    else:
        text = get_message_by_name_for_user(name="video_instruction", telegram_id=user_id).text
        keyboard = await ik.get_video_menu()
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state
    )
