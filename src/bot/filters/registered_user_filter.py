from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from apps.profiles.services import profile
from bot.data import list_and_tuple_data as ld


class IsRegistered(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                user_id = message.from_user.id
                user_profile = profile.get_profile_by_telegram_id(user_id)
                return True if user_profile else False
            case types.CallbackQuery:
                user_id = message.message.from_user.id
                user_profile = profile.get_profile_by_telegram_id(user_id)
                return True if user_profile else False
            case _:
                return False


class NotRegistered(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                user_id = message.from_user.id
                user_profile = profile.get_profile_by_telegram_id(user_id)
                return True if not user_profile else False
            case types.CallbackQuery:
                user_id = message.message.from_user.id
                user_profile = profile.get_profile_by_telegram_id(user_id)
                return True if not user_profile else False
            case _:
                return False