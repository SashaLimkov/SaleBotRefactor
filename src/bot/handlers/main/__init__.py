from aiogram import Dispatcher
from aiogram.dispatcher import filters
from bot.filters.admin_filter import IsAdmin

from bot.handlers.main import registration_module
from bot.handlers.main import commands


def setup(dp: Dispatcher):
    registration_module.setup(dp)
    dp.register_message_handler(commands.start_command, filters.CommandStart(), IsAdmin(), state="*")
