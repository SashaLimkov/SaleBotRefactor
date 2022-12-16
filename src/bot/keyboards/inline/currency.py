from apps.settings.services.currency import get_list_currency
from bot.utils.keyboard_utils.base_keyboard_utils import (
    get_base_keyboard,
    get_inline_button,
)
from bot.data import callback_data as cd

__all__ = [
    "get_main_currency_settings_menu",
    "get_custom_currency_menu",
    "cancel_customize_selected_currency",
]


async def get_main_currency_settings_menu(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 2,
        },
    )
    keyboard.insert(
        await get_inline_button(
            text="RUB",
            cd=cd.settings_currency.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=1,
            ),
        )
    )
    keyboard.insert(
        await get_inline_button(
            text="Валюта сайта",
            cd=cd.settings_currency.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=0,
            ),
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Задать курс",
            cd=cd.settings_currency.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=2,
            ),
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.mm.new(action=callback_data["first_lvl"])
        )
    )
    return keyboard


async def get_custom_currency_menu(callback_data: dict):
    currency_list = get_list_currency()
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 4,
        },
    )
    for currency in currency_list:
        if currency.currency in ("RUB", "ALL"):
            continue
        keyboard.insert(
            await get_inline_button(
                text=currency.name,
                cd=cd.select_customize_currency.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=callback_data["third_lvl"],
                    selected_cur=currency.currency,
                ),
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад",
            cd=cd.settings_menu.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
            ),
        )
    )
    return keyboard


async def cancel_customize_selected_currency(callback_data: dict):
    return await get_base_keyboard(
        buttons=[
            {
                "text": "Отмена",
                "callback_data": cd.settings_currency.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=callback_data["third_lvl"],
                ),
            }
        ],
        keyboard_options={
            "row_width": 1,
        },
    )
