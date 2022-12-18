from apps.settings.services.settings_product_user import get_product_settings
from apps.settings.services.settings_user import get_settings
from bot.utils.keyboard_utils.base_keyboard_utils import (
    get_base_keyboard,
    get_inline_button,
)
from bot.data import callback_data as cd

__all__ = [
    "get_select_compilation_menu",
]


async def get_select_compilation_menu(callback_data: dict):
    buttons = [
        {
            "text": "Выбрать подборку",
            "switch_inline_query_current_chat": "",
        },
        {
            "text": "◀ Назад",
            "callback_data": cd.mm.new(action=callback_data["first_lvl"])
        }
    ]
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 1,
        }
    )
