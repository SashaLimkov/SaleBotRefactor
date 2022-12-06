from bot.config import bot
from bot.data import list_and_tuple_data as ld


async def notice_programmers(exception_info):
    for user_id in ld.ADMINS:
        await bot.send_message(
            chat_id=user_id,
            text=f"Ошибка в боте {await bot.me().username}:\n{exception_info}",
        )
