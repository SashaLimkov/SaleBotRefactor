from apps.settings.services.settings_product_user import get_product_settings
from apps.settings.services.settings_user import get_settings
from bot.utils.keyboard_utils.base_keyboard_utils import (
    get_base_keyboard,
    get_inline_button,
)
from bot.data import callback_data as cd

__all__ = ["get_link_settings_menu"]


async def get_link_settings_menu(callback_data: dict, telegram_id: int):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    settings = get_settings(telegram_id=telegram_id)
    if settings.link:
        keyboard.add(
            await get_inline_button(
                text="Короткая ссылка ✅",
                cd=cd.settings_link.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="link",
                ),
            )
        )
        keyboard.add(await get_inline_button(text="Ссылка в тексте ❌", cd="..."))
    elif settings.hided_link:
        keyboard.add(await get_inline_button(text="Короткая ссылка ❌", cd="..."))
        keyboard.add(
            await get_inline_button(
                text="Ссылка в тексте ✅",
                cd=cd.settings_link.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="hided_link",
                ),
            )
        )
    else:
        keyboard.add(
            await get_inline_button(
                text="Короткая ссылка ⬜",
                cd=cd.settings_link.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="link",
                ),
            )
        )
        keyboard.add(
            await get_inline_button(
                text="Ссылка в тексте ⬜",
                cd=cd.settings_link.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="hided_link",
                ),
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.mm.new(action=callback_data["first_lvl"])
        )
    )
    return keyboard
