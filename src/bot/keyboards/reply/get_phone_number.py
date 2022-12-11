from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard


async def get_user_contact():
    return await get_base_keyboard(
        buttons=[
            {
                "text": "Отправить номер",
                "request_contact": True
            },
        ],
        keyboard_options={
            "resize_keyboard": True,
        },
        is_inline=False
    )
