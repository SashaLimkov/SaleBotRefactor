import traceback

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from apps.message.services.message import get_message_by_name_for_user
from bot.config import bot
from bot.keyboards import inline as ik
from bot.utils.notice_programmers import notice_programmers


async def start_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    main_message_id = data.get("main_message_id", False)
    user_id = message.from_user.id
    start_registration_text = get_message_by_name_for_user(name="start_registration")
    if main_message_id:
        try:
            await bot.edit_message_text(
                chat_id=user_id,
                text=start_registration_text.text,
                message_id=main_message_id,
                reply_markup=await ik.get_start_registration_keyboard()
            )
        except exceptions.MessageNotModified:
            await notice_programmers(exception_info=traceback.format_exc(), **message.from_user.to_python())
        except Exception:
            await notice_programmers(exception_info=traceback.format_exc(), **message.from_user.to_python())

    else:
        mes = await bot.send_message(
            chat_id=user_id,
            text=start_registration_text.text,
            reply_markup=await ik.get_start_registration_keyboard()
        )
        await state.update_data({"main_message_id": mes.message_id})
