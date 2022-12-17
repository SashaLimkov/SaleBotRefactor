from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from apps.profiles.services import subscription
from apps.profiles.services.profile import get_profile_by_telegram_id
from bot.data import list_and_tuple_data as ld


class IsTrial(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                user_id = message.from_user.id
                user_sub_price = subscription.get_user_active_subscription(telegram_id=user_id).rate.price
                return int(user_sub_price) == 0
            case types.CallbackQuery:
                user_id = message.message.chat.id
                user_sub_price = subscription.get_user_active_subscription(telegram_id=user_id).rate.price
                return int(user_sub_price) == 0
            case _:
                return False


class IsNotTrial(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                user_id = message.from_user.id
                user_sub_price = subscription.get_user_active_subscription(telegram_id=user_id).rate.price
                return int(user_sub_price) != 0
            case types.CallbackQuery:
                user_id = message.message.chat.id
                user_sub_price = subscription.get_user_active_subscription(telegram_id=user_id).rate.price
                return int(user_sub_price) != 0
            case _:
                return False


class IsHelper(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                user_id = message.from_user.id
                is_helper = get_profile_by_telegram_id(telegram_id=user_id).is_helper
                return is_helper
            case types.CallbackQuery:
                user_id = message.message.chat.id
                is_helper = get_profile_by_telegram_id(telegram_id=user_id).is_helper
                return is_helper
            case _:
                return False
