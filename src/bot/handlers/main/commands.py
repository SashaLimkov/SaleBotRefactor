from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_by_telegram_id
from bot.config import bot
from bot.handlers.main.posts.date_and_inline import cleaner
from bot.states.MainMenu import MainMenu
from bot.utils.deleter import try_delete_message
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik


async def start_command(message: types.Message, state: FSMContext):
    await MainMenu.MAIN_MENU.set()
    data = await state.get_data()
    user_id = message.chat.id
    await cleaner(state=state, user_id=user_id)
    user = get_profile_by_telegram_id(telegram_id=user_id)
    text = get_message_by_name_for_user(
        name="main_menu_message", telegram_id=user_id
    ).text.format(name=user.first_name)
    await message.delete()
    await mw.try_send_message(
        user_id=user_id,
        text=text,
        message=message,
        state=state,
        keyboard=await ik.get_main_menu(user.in_chat),
    )


async def anons(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    callback_data = data.get("callback_data")
    text = get_message_by_name_for_user(
        name="select_date", telegram_id=user_id
    ).text
    keyboard = await ik.get_date_menu(callback_data=callback_data)
    await try_delete_message(
        chat_id=user_id,
        message_id=message.message_id
    )
    await mw.try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        keyboard=keyboard,
        main_message_id=main_message_id,
        state=state
    )
