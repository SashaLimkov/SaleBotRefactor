from apps.settings.services.settings_product_user import get_product_settings
from bot.utils.keyboard_utils.base_keyboard_utils import (
    get_base_keyboard,
    get_inline_button,
)
from bot.data import callback_data as cd
from bot.data import list_and_tuple_data as ld

__all__ = ["get_product_settings_menu"]


async def get_product_settings_menu(callback_data: dict, telegram_id: int):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    settings = get_product_settings(telegram_id=telegram_id)
    data_dict = {
        "Ссылка": settings.link,
        "Название": settings.name,
        "Цена": settings.price,
        "Скидка": settings.discount,
        "Размеры": settings.sizes,
        "Описание": settings.description,
    }
    callback = {
        "Ссылка": "link",
        "Название": "name",
        "Цена": "price",
        "Скидка": "discount",
        "Размеры": "sizes",
        "Описание": "description",
    }
    for key, value in data_dict.items():
        keyboard.add(
            await get_inline_button(
                text=f"{key} {'✅' if value else '⬜'}",
                cd=cd.settings_product.new(
                    first_lvl=callback_data["first_lvl"],
                    second_lvl=callback_data["second_lvl"],
                    third_lvl=callback[key],
                ),
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.mm.new(action=callback_data["first_lvl"])
        )
    )
    return keyboard
