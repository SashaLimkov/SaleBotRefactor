from bot.config import bot
from bot.utils.notice_programmers import notice_programmers


async def try_delete_message(chat_id: str | int, message_id: str | int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        await notice_programmers(exception_info=e)
