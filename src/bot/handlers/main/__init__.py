from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.data.list_and_tuple_data import ADMINS
from bot.handlers.main import commands, registration_module, subscriptions, main_menu_actions, user_settings, channels, \
    posts


def setup(dp: Dispatcher):
    registration_module.setup(dp)
    subscriptions.setup(dp)
    main_menu_actions.setup(dp)
    user_settings.setup(dp)
    channels.setup(dp)
    posts.setup(dp)
    dp.register_message_handler(
        commands.anons, filters.CommandStart(deep_link="select_section"), state="*"
    )
    dp.register_message_handler(
        commands.fix_users,
        filters.Command("fix_users"),
        lambda message: message.chat.id in ADMINS,
        state="*"
    )
    dp.register_message_handler(
        commands.start_command, filters.CommandStart(), state="*"
    )
