from apps.settings.services.settings_user import get_settings
from bot.utils.keyboard_utils.base_keyboard_utils import (
    get_base_keyboard,
    get_inline_button,
)
from bot.data import callback_data as cd

__all__ = ["get_wm_add_logo_menu", "cancel_updating_logo_or_t_logo", "logo_settings"]


async def get_wm_add_logo_menu(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Добавить фото",
            cd=cd.settings_wm.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=0,
            ),
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Добавить текст",
            cd=cd.settings_wm.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=1,
            ),
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.mm.new(action=callback_data["first_lvl"])
        )
    )
    return keyboard


async def cancel_updating_logo_or_t_logo(callback_data: dict):
    return await get_base_keyboard(
        buttons=[
            {
                "text": "Отмена",
                "callback_data": cd.settings_menu.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                ),
            }
        ],
        keyboard_options={
            "row_width": 1,
        },
    )


async def logo_settings(callback_data: dict, telegram_id: int):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 2,
        },
    )
    user_settings = get_settings(telegram_id=telegram_id)
    if user_settings.logo_position == "center":
        keyboard.insert(
            await get_inline_button(
                text="✅ По центру",
                cd=cd.settings_wm_position.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="off",
                ),
            )
        )
        keyboard.insert(
            await get_inline_button(
                text="❌ По всему фото",
                cd=cd.settings_wm_position.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="...",
                ),
            )
        )
    elif user_settings.logo_position == "fill":
        keyboard.insert(
            await get_inline_button(
                text="❌ По центру",
                cd=cd.settings_wm_position.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="...",
                ),
            )
        )
        keyboard.insert(
            await get_inline_button(
                text="✅ По всему фото",
                cd=cd.settings_wm_position.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="off",
                ),
            )
        )
    else:
        keyboard.insert(
            await get_inline_button(
                text="⬜ По центру",
                cd=cd.settings_wm_position.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="center",
                ),
            )
        )
        keyboard.insert(
            await get_inline_button(
                text="⬜ По всему фото",
                cd=cd.settings_wm_position.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl="fill",
                ),
            )
        )
    keyboard.add(
        await get_inline_button(
            text="Изменить водяной знак",
            cd=cd.settings_wm_position.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl="remove",
            ),
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.mm.new(action=callback_data["first_lvl"])
        )
    )
    return keyboard
