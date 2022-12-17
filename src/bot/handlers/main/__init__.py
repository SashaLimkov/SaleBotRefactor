from aiogram import Dispatcher
from aiogram.dispatcher import filters
from bot.filters import IsAdmin, IsRegistered

from bot.handlers.main import registration_module, main_menu_actions, user_settings, channels, subscriptions
from bot.handlers.main import commands


def setup(dp: Dispatcher):
    registration_module.setup(dp)
    main_menu_actions.setup(dp)
    user_settings.setup(dp)
    channels.setup(dp)
    subscriptions.setup(dp)
    dp.register_message_handler(
        commands.start_command, filters.CommandStart(), IsRegistered(), state="*"
    )
