from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_is_helper
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw


async def sub_or_add_helper_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict = {}):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["second_lvl"])
    if user_action:
        text = get_message_by_name_for_user(name="add_helper", telegram_id=user_id).text
        keyboard = await ik.get_helper_subscription_to_buy(callback_data=callback_data, telegram_id=user_id)
    else:
        is_helper = get_profile_is_helper(telegram_id=user_id)
        text = get_message_by_name_for_user(name="buy_sub", telegram_id=user_id).text
        keyboard = await ik.get_subscriptions_list_to_buy(callback_data=callback_data, is_helper=is_helper)
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        keyboard=keyboard,
        text=text,
        main_message_id=main_message_id,
        state=state
    )
