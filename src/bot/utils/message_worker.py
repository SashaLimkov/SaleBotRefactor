import traceback

import cv2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from bot.config import bot
from bot.utils.deleter import try_delete_message
from bot.utils.notice_programmers import notice_programmers


async def try_edit_message(
    message, user_id, text, main_message_id, keyboard, state: FSMContext
):
    """
    Функция, которая пытается обновить любое текстовое сообщение по main_message_id.
    :param message:
    :param user_id:
    :param text:
    :param main_message_id:
    :param keyboard:
    :param state:
    :return:
    """
    try:
        await bot.edit_message_text(
            chat_id=user_id,
            text=text,
            message_id=main_message_id,
            reply_markup=keyboard if keyboard else None,
        )
    except exceptions.MessageNotModified:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.from_user.to_python()
        )
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.from_user.to_python()
        )
        await message.delete()
        await try_send_message(message, user_id, text, keyboard, state)


async def try_send_message(message, user_id, text, keyboard, state: FSMContext):
    """Функция, которая пытается отправить любое текстовое сообщение.
    С учетом main_message_id для дальнейшего его обновления.
    Удаляет предыдущее главное сообщение.
    :param message:
    :param user_id:
    :param text:
    :param keyboard:
    :param state:
    :return:
    """
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    await try_delete_message(user_id, main_message_id)
    try:
        mes = await bot.send_message(
            chat_id=user_id, text=text, reply_markup=keyboard if keyboard else None
        )
        await state.update_data({"main_message_id": mes.message_id})
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.chat.to_python()
        )


async def try_send_video(
    video_path,
    chat_id: int,
    text,
    message,
    state: FSMContext,
    keyboard,
    splited_message: bool = False,
):
    """
    Функция, которая пытается отправить видео по пути к нему. Отправляет с учетом мета-данных о видео.
    Также имеется возможность прикрутить описание к видео либо в этом же сообщении, либо в раздельном.
    :param video_path:
    :param chat_id:
    :param text:
    :param message:
    :param state:
    :param keyboard:
    :param splited_message:
    :return:
    """
    vid = cv2.VideoCapture(video_path)
    wh, hh = vid.get(cv2.CAP_PROP_FRAME_WIDTH), vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    try:
        await bot.send_video(
            chat_id=chat_id,
            width=wh,
            height=hh,
            supports_streaming=True,
            video=types.InputFile(video_path),
            caption=text if not splited_message else "",
        )
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.from_user.to_python()
        )
    if splited_message:
        await try_send_message(
            message=message,
            user_id=chat_id,
            text=text,
            keyboard=keyboard if keyboard else None,
            state=state,
        )
