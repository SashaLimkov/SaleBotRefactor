from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard

__all__ = [
    "get_start_registration_keyboard",
]


async def get_start_registration_keyboard():
    return await get_base_keyboard(
        buttons=[
            {
                "text": "Начать регистрацию",
                "callback_data": "start_reg"
            },
        ]
    )


async def get_user_registration_menu():
    pass
