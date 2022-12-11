from bot.config import bot
from bot.data import list_and_tuple_data as ld


async def notice_programmers(exception_info, **kwargs):
    user_info = "\n"
    for key, val in kwargs.items():
        user_info += f"{key} : {val}\n"
    await bot.send_message(
        chat_id=ld.ADMIN_GROUP[0],
        text=f"Пользователь: {user_info}\nОшибка в боте:\n{exception_info}",
    )
