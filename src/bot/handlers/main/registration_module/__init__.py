from aiogram import Dispatcher, types
from aiogram.dispatcher import filters

from bot.filters import NotRegistered
from bot.handlers.main.registration_module import user_registration


def setup(dp: Dispatcher):
    dp.register_message_handler(user_registration.start_registration, filters.CommandStart(), NotRegistered(),
                                state="*")

    dp.register_message_handler(user_registration.get_user_contact, content_types=types.ContentTypes.CONTACT, state="*")
