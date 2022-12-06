from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot.data import list_and_tuple_data as ld


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                return message.chat.id in ld.ADMINS
            case types.CallbackQuery:
                return message.message.chat.id in ld.ADMINS
            case _:
                return False
