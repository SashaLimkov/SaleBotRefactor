from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd

__all__ = [
    "get_signature_menu",
    "cancel_signature_editing"
]


async def get_signature_menu(callback_data: dict, user_signature: str):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    if user_signature:
        keyboard.add(
            await get_inline_button(
                text="Изменить подпись",
                cd=cd.settings_signature.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=0,
                )
            )
        )
        keyboard.add(
            await get_inline_button(
                text="Удалить подпись",
                cd=cd.settings_signature.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=1,
                )
            )
        )
    else:
        keyboard.add(
            await get_inline_button(
                text="Добавить подпись",
                cd=cd.settings_signature.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=0,
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


async def cancel_signature_editing(callback_data: dict):
    return await get_base_keyboard(
        buttons=[
            {
                "text": "Отмена",
                "callback_data": cd.settings_menu.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                )
            }
        ],
        keyboard_options={
            "row_width": 1,
        },
    )
