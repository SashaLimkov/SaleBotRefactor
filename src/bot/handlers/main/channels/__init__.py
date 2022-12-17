from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.data import callback_data as cd
from bot.handlers.main.channels import work_with_sys_messages


def setup(dp: Dispatcher):
    # Возможно бесполезный хэндлер. Никогда не отрабатывает.
    dp.register_message_handler(
        work_with_sys_messages.delete_system_message_in_main_channel,
        content_types=["new_chat_members", "left_chat_member"],
    )
    dp.register_my_chat_member_handler(
        work_with_sys_messages.fix_my_chats,
    )
