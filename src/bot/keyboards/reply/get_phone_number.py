from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard

__all__ = [
    "get_user_contact",
]


async def get_user_contact():
    keyboard = await get_base_keyboard(
        buttons=[
            {"text": "Отправить номер", "request_contact": True},
        ],
        keyboard_options={
            "resize_keyboard": True,
        },
        is_inline=False,
    )
    print(keyboard)
    return keyboard
