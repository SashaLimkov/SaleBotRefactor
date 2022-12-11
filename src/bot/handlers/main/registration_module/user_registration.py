from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from bot.config import bot
from bot.keyboards import inline as ik


async def start_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    main_message_id = data.get("main_message_id", False)
    user_id = message.from_user.id
    start_registration_text = "saasdasd"  # get_message_by_name_for_user(name="start_registration", telegram_id=user_id)
    if main_message_id:
        await bot.edit_message_text(
            chat_id=user_id,
            text=start_registration_text.text
        )
    else:
        mes = await bot.send_message(
            chat_id=user_id,
            text=start_registration_text.text,
            reply_markup=await ik.get_start_registration_keyboard()
        )
        await state.update_data({"main_message_id": mes.message_id})
