from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd

__all__ = [
    "get_channels_menu",
    "get_channels_list"
]


async def get_channels_menu(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="VK",
            url="https://vk.me/public215772054?ref=390959255&ref_source=390959255"
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Telegram",
            cd=cd.settings_channel.new(
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


async def get_channels_list(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад",
            cd=cd.settings_menu.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"]
            )
        ))
    return keyboard
