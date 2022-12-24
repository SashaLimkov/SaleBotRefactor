from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_by_telegram_id
from bot.handlers.main.main_menu_actions.main_menu import main_menu_actions
from bot.utils.user import get_user_days
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw


async def sub_ended(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(2323232323232323)
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    days = await get_user_days(telegram_id=user_id)
    text = get_message_by_name_for_user(
        name="check_cub", telegram_id=user_id
    ).text.format(sub_days=days)
    user = get_profile_by_telegram_id(user_id)
    keyboard = await ik.get_sub_menu(
        is_active=user.is_active,
        is_helper=user.is_helper,
        callback_data={"action": 3},
        ended_sub=True,
    )

    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        main_message_id=main_message_id,
        text=text,
        state=state,
        keyboard=keyboard
    )