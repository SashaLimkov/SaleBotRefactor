from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.handlers.main.main_menu_actions.main_menu import main_menu_actions


async def sub_ended(call: types.CallbackQuery, state: FSMContext):
    callback_data = {
        "action": 3,

    }
    await main_menu_actions(call=call, callback_data=callback_data, state=state, ended_sub=True)
