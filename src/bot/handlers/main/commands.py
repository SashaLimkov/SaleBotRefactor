from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_by_telegram_id
from bot.config import bot
from bot.states.MainMenu import MainMenu
from bot.utils.deleter import try_delete_message
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik


async def start_command(message: types.Message, state: FSMContext):
    await MainMenu.MAIN_MENU.set()
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    user = get_profile_by_telegram_id(telegram_id=user_id)
    text = get_message_by_name_for_user(name="confirm_registration", telegram_id=user_id).text.format(
        name=user.first_name)
    await message.delete()
    await mw.try_send_message(
        user_id=user_id,
        text=text,
        message=message,
        state=state,
        keyboard=await ik.get_main_menu(user.in_chat)
    )
