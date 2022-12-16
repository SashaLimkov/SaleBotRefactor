from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from bot.utils import message_worker as mw
from apps.settings.services.settings_user import update_field_settings
from bot.keyboards import inline as ik


async def select_rounder_lvl(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    selected_round_lvl = int(callback_data["third_lvl"])
    update_field_settings(
        telegram_id=user_id, field="rounder", value=selected_round_lvl
    )
    call_text = get_message_by_name_for_user(
        name="select_round_lvl", telegram_id=user_id
    ).text.format(selected_rounder=selected_round_lvl)
    await call.answer(text=call_text, show_alert=True)
    text = get_message_by_name_for_user(name="rounder_settings").text.format(
        selected_rounder=selected_round_lvl
    )
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=await ik.get_rounder_settings_menu(callback_data=callback_data),
        state=state,
    )
