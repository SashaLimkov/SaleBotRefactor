from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from bot.handlers.main.subscriptions.buy_sub_or_add_helper import sub_or_add_helper_menu


async def not_allowed_at_trial(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = call.message.chat.id
    user_action = int(callback_data["second_lvl"])
    if user_action:
        text = get_message_by_name_for_user(name="cant_add_helper_on_trial", telegram_id=user_id).text
        await call.answer(text=text, show_alert=True)
    else:
        await sub_or_add_helper_menu(call=call, callback_data=callback_data, state=state)


async def not_allowed_helper(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = call.message.chat.id
    user_action = int(callback_data["second_lvl"])
    if user_action:
        text = get_message_by_name_for_user(name="cant_add_helper_helper", telegram_id=user_id).text
        await call.answer(text=text, show_alert=True)
    else:
        await sub_or_add_helper_menu(call=call, callback_data=callback_data, state=state)
