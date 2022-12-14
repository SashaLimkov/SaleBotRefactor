from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd

__all__ = [
    "get_formula_commission",
    "cancel_commission_editing"
]


async def get_formula_commission(callback_data: dict, selected_formula):
    keyboard = await get_base_keyboard(keyboard_options={
        "row_width": 1,
    })
    if selected_formula:
        keyboard.add(
            await get_inline_button(
                text="Выбрать формулу без комиссии",
                cd=cd.settings_formula_and_comm.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=0,
                )
            )
        )
        keyboard.add(
            await get_inline_button(
                text="Изменить размер комиссии",
                cd=cd.settings_formula_and_comm.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=2,
                )
            )
        )
    else:
        keyboard.add(
            await get_inline_button(
                text="Выбрать формулу с комиссией",
                cd=cd.settings_formula_and_comm.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=1,
                )
            )
        )
    keyboard.add(await get_inline_button(
        text="◀ Назад",
        cd=cd.mm.new(
            action=callback_data["first_lvl"]
        )
    ))
    return keyboard


async def cancel_commission_editing(callback_data: dict):
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
