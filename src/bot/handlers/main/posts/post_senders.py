from aiogram import types
from aiogram.dispatcher import FSMContext
from apps.message.services.message import get_message_by_name_for_user
from apps.posts.services.compilation import get_list_compilations_by_date, get_compilation_by_id, get_final_compilation
from apps.posts.services.post import get_formatted_user_settings_posts_by_compilation_id
from bot.handlers.main.posts.posts import send_compilation, send_final_compilation
from bot.utils import message_worker as mw, deleter
from bot.keyboards import inline as ik


async def send_posts(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    user_id = call.message.chat.id
    channel_id = int(callback_data["channel_id"])
    send_compilation_list = data.get("send_compilation_list")
    send_post_pk_list = data.get("send_post_pk_list")
    send_all = int(callback_data["send_one_or_all"])
    compilation = int(callback_data["comp_or_post"])
    obj_id = int(callback_data["post_id"])
    platform = callback_data["platform"]
    text = get_message_by_name_for_user(name='sending_started', telegram_id=user_id).text
    await call.answer(
        text=text,
        show_alert=True
    )
    if platform == "tg":
        if compilation and not send_all:
            print(compilation)
            print(obj_id)
            if compilation == 2:
                await send_final_compilation(
                    compilation_id=obj_id,
                    chat_id=channel_id,
                    message=call.message,
                    keyboard=None
                )
            else:
                await send_compilation(
                    compilation_id=obj_id,
                    chat_id=channel_id,
                    message=call.message,
                    keyboard=None
                )
        else:
            compilation_id = int(data.get("compilation_id"))
            posts = get_formatted_user_settings_posts_by_compilation_id(compilation_id=compilation_id,
                                                                        telegram_id=user_id, )
            if send_all:
                if compilation_id in send_compilation_list:
                    await send_compilation(
                        compilation_id=compilation_id,
                        chat_id=channel_id,
                        message=call.message,
                        keyboard=None
                    )
                for post in posts:
                    if post[2] in send_post_pk_list:
                        await send_post(post=post, channel_id=channel_id, message=call.message)

                if get_final_compilation(compilation_id=compilation_id):
                    await send_final_compilation(
                        compilation_id=compilation_id,
                        chat_id=channel_id,
                        message=call.message,
                        keyboard=None
                    )
            else:
                for post in posts:
                    if post[-1] == obj_id:
                        await send_post(post=post, channel_id=channel_id, message=call.message)
                        break


async def send_post(post, channel_id: int, message: types.Message):
    text = post[0]
    media = post[1][0]
    media_type: int = media[0]
    media_path = media[1]
    await mw.try_send_post_to_user(
        file_path=media_path,
        file_type=media_type,
        chat_id=channel_id,
        text=text,
        message=message,
        keyboard=None
    )
