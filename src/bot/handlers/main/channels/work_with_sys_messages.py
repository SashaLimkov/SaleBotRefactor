import traceback

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_by_telegram_id, get_profile_is_helper
from apps.profiles.services.subscription import get_user_active_subscription
from apps.settings.services.chanel import delete_channel_telegram, add_channel_telegram, get_list_telegram_channels
from bot.states.MainMenu import MainMenu
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik
from bot.utils.notice_programmers import notice_programmers
from core.settings import CHANNEL


async def delete_system_message_in_main_channel(message: types.Message):
    try:
        print(123)
        await mw.try_delete_message(chat_id=CHANNEL, message_id=message.message_id)
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(),
            **message.chat.to_python()
        )


async def fix_my_chats(update: types.ChatMemberUpdated):
    channel_id = update.chat.id
    user_id = update.from_user.id
    if update.new_chat_member.status == "left" or update.new_chat_member.status == "kicked":
        channels = get_list_telegram_channels(telegram_id=user_id)
        for channel in channels:
            if channel.chat_id == channel_id:
                delete_channel_telegram(
                    telegram_id=user_id,
                    channel_id=channel_id,
                )
    else:
        if not get_profile_is_helper(telegram_id=user_id):
            add_channel_telegram(
                telegram_id=user_id,
                name=update.chat.full_name,
                channel_id=channel_id
            )
