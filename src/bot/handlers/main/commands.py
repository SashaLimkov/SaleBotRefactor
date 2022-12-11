from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config import bot
from bot.utils.deleter import try_delete_message


async def start_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    if main_message_id:
        await message.delete()
        await try_delete_message(chat_id=message.chat.id, message_id=main_message_id)
    mes = await bot.send_message(
        chat_id=message.chat.id,
        text="алло",
    )
    await state.update_data({"main_message_id": mes.message_id})
