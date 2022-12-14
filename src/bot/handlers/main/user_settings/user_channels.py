from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.settings.services.chanel import get_list_telegram_channels
from bot.utils import message_worker as mw
from apps.settings.services.settings_user import update_field_settings
from bot.keyboards import inline as ik


async def get_tg_channels_and_instructions(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    text = get_message_by_name_for_user(
        name="tg_channel_instructions",
        telegram_id=user_id).text.format(channels_list=await get_tg_channels_list_text(telegram_id=user_id))
    keyboard = await ik.get_channels_list(callback_data=callback_data)
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def get_tg_channels_list_text(telegram_id: int) -> str:
    tg_channels = get_list_telegram_channels(telegram_id=telegram_id)
    channel_list = ""
    for channel in tg_channels:
        channel_list += f"{channel.name}\n"
    return channel_list
