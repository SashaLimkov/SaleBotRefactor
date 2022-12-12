from bot.utils.datetime_helper import get_datetime
from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard
from bot.data import callback_data as cd
from bot.data import list_and_tuple_data as ld

__all__ = [
    "get_main_currency_settings_menu",
    "get_rounder_settings_menu"
]


async def get_main_currency_settings_menu(callback_data: dict):
    buttons = [
        {
            "text": "RUB",
            "callback_data": "..."
        },
        {
            "text": "Валюта сайта",
            "callback_data": "..."
        },
        {
            "text": "Задать курс",
            "callback_data": "..."
        },
        {"text": "◀ Назад", "callback_data": cd.mm.new(
            action=callback_data["first_lvl"]
        )}
    ]
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 2,
        },
    )


async def get_rounder_settings_menu(callback_data: dict):
    buttons = [
        {
            "text": "1",
            "callback_data": "..."
        },
        {
            "text": "2",
            "callback_data": "..."
        },
        {
            "text": "3",
            "callback_data": "..."
        },
        {
            "text": "4",
            "callback_data": "..."
        },
        {
            "text": "Без округления",
            "callback_data": "..."
        },
        {"text": "◀ Назад", "callback_data": cd.mm.new(
            action=callback_data["first_lvl"]
        )}
    ]
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 2,
        },
    )
