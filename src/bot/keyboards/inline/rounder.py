from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd

__all__ = [
    "get_rounder_settings_menu"
]


async def get_rounder_settings_menu(callback_data: dict):
    buttons = [
        {
            "text": "1",
            "callback_data": cd.settings_rounder.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=1
            )
        },
        {
            "text": "2",
            "callback_data": cd.settings_rounder.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=2
            )
        },
        {
            "text": "3",
            "callback_data": cd.settings_rounder.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=3
            )
        },
        {
            "text": "4",
            "callback_data": cd.settings_rounder.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=4
            )
        }
    ]
    keyboard = await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 2,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Без округления",
            cd=cd.settings_rounder.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=0
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад",
            cd=cd.mm.new(
                action=callback_data["first_lvl"]
            )
        ))
    return keyboard
