import traceback
import unicodedata
from html import unescape

import cv2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions
from aiogram.utils.exceptions import MessageNotModified

from bot.config import bot
from bot.utils.deleter import try_delete_message
from bot.utils.notice_programmers import notice_programmers
from core import settings


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
    except Exception:
        await try_send_message(message, user_id, text, keyboard, state)
        await try_delete_message(
            chat_id=user_id,
            message_id=main_message_id,
        )


async def try_send_invoice(message, user_id, keyboard, state, main_message_id, **kwargs):
    try:
        await try_delete_message(
            chat_id=user_id,
            message_id=main_message_id
        )

        mes = await bot.send_invoice(
            chat_id=user_id,
            **kwargs,
        )
        await state.update_data({"main_message_id": mes.message_id})
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.chat.to_python()
        )


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
        return mes.message_id
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.chat.to_python()
        )


async def send_confirmed_message(chat_id: int, text: str):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
        )
    except Exception as e:
        print(e)


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


async def try_edit_photo(
        photo_path,
        chat_id: int,
        text,
        message,
        main_message_id,
        state: FSMContext,
        keyboard,
):
    """
    Функция, которая пытается отправить видео по пути к нему. Отправляет с учетом мета-данных о видео.
    Также имеется возможность прикрутить описание к видео либо в этом же сообщении, либо в раздельном.
    :param photo_path:
    :param chat_id:
    :param text:
    :param message:
    :param state:
    :param keyboard:
    :param main_message_id:
    :return:
    """
    try:
        await bot.edit_message_caption(
            chat_id=chat_id,
            caption=text,
            message_id=main_message_id,
            reply_markup=keyboard
        )
    except Exception:
        await try_send_photo(
            photo_path=photo_path,
            chat_id=chat_id,
            text=text,
            message=message,
            main_message_id=main_message_id,
            state=state,
            keyboard=keyboard
        )


async def try_send_photo(
        photo_path,
        chat_id: int,
        text,
        message,
        main_message_id,
        state: FSMContext,
        keyboard,
):
    """
    Функция, которая пытается отправить видео по пути к нему. Отправляет с учетом мета-данных о видео.
    Также имеется возможность прикрутить описание к видео либо в этом же сообщении, либо в раздельном.
    :param photo_path:
    :param chat_id:
    :param text:
    :param message:
    :param state:
    :param keyboard:
    :param main_message_id:
    :return:
    """
    try:
        await try_delete_message(
            chat_id=chat_id,
            message_id=main_message_id,
        )
        mes = await bot.send_photo(
            chat_id=chat_id,
            photo=types.InputFile(photo_path),
            caption=text,
            reply_markup=keyboard
        )
        await state.update_data(main_message_id=mes.message_id)
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.from_user.to_python()
        )


async def try_send_post_to_user(
        file_path: str,
        file_type: int,
        chat_id: int,
        text: str,
        message=None,
        keyboard=None,
        message_id: int = 0):
    text = unicodedata.normalize('NFKC', unescape(text.replace('<br>', '\n')))
    if file_type:
        mes_id = await try_send_post_with_video(file_path=file_path, chat_id=chat_id, text=text, message=message,
                                                keyboard=keyboard, message_id=message_id)
    else:
        mes_id = await try_send_post_with_photo(file_path=file_path, chat_id=chat_id, text=text, message=message,
                                                keyboard=keyboard, message_id=message_id)
    return mes_id


async def try_send_post_with_photo(
        file_path: str,
        chat_id: int,
        text: str,
        message,
        keyboard,
        message_id: int, ):
    try:
        if message_id:
            file = types.InputMedia(media=types.InputFile(file_path), caption=text, parse_mode="HTML")
            mes = await bot.edit_message_media(
                chat_id=chat_id,
                media=file,
                reply_markup=keyboard,
                message_id=message_id
            )
        else:
            mes = await bot.send_photo(
                chat_id=chat_id,
                photo=types.InputFile(file_path),
                caption=text,
                reply_markup=keyboard
            )
        return mes.message_id
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.from_user.to_python()
        )


async def try_send_post_with_video(
        file_path: str,
        chat_id: int,
        text: str,
        message,
        keyboard,
        message_id: int, ):
    try:
        vid = cv2.VideoCapture(file_path)
        wh, hh = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if message_id:
            file = types.InputMedia(media=types.InputFile(file_path), caption=text, type="video",
                                    supports_streaming=True, width=wh,
                                    height=hh, parse_mode="HTML")
            mes = await bot.edit_message_media(
                chat_id=chat_id,
                media=file,
                reply_markup=keyboard,
                message_id=message_id
            )
        else:
            mes = await bot.send_video(
                chat_id=chat_id,
                video=types.InputFile(file_path),
                width=wh,
                height=hh,
                supports_streaming=True,
                caption=text,
                reply_markup=keyboard
            )
        return mes.message_id
    except Exception:
        await notice_programmers(
            exception_info=traceback.format_exc(), **message.from_user.to_python()
        )


async def try_pin_unpin_message(chat_id: int, message_id: int, pin: bool):
    try:
        if pin:
            await bot.pin_chat_message(
                chat_id=chat_id,
                message_id=message_id
            )
        else:
            await bot.unpin_chat_message(
                chat_id=chat_id,
                message_id=message_id
            )
    except:
        await notice_programmers(exception_info=traceback.format_exc())


async def try_edit_keyboard(
        chat_id: int,
        message_id: int,
        keyboard):
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard
        )
    except:
        await notice_programmers(
            exception_info=traceback.format_exc(),
        )


async def try_edit_message_caption(
        chat_id: int,
        text: str,
        message_id: int,
        keyboard, ):
    try:
        await bot.edit_message_caption(
            chat_id=chat_id,
            caption=text,
            message_id=message_id,
            reply_markup=keyboard
        )
    except:
        await notice_programmers(
            exception_info=traceback.format_exc(),
        )
