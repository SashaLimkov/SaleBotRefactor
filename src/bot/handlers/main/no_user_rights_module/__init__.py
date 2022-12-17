from aiogram import Dispatcher

from bot.data import callback_data as cd
from bot.filters import IsTrial, IsHelper
from bot.handlers.main.no_user_rights_module import add_helper


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_helper.not_allowed_at_trial,
        IsTrial(),
        cd.sub_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        add_helper.not_allowed_helper,
        IsHelper(),
        cd.sub_menu.filter(),
        state="*"
    )

