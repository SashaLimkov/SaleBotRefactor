from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.posts.services.compilation import get_compilation_by_id
from apps.posts.services.post import get_formatted_user_settings_posts_by_compilation_id, add_user_post
from bot.keyboards import inline as ik
from bot.states.MainMenu import MainMenu
from bot.states.Posts import PostStates
from bot.utils import message_worker as mw


async def sender_anons(message: types.Message, state: FSMContext):
    data = await state.get_data()
    callback_data = data.get("callback_data")
    main_message_id = data.get("main_message_id", False)
    delete_messages_list = []
    send_post_pk_list = []
    user_id = message.chat.id
    compilation_id = int(message.text.split("|:|")[-1])
    send_compilation_list = [compilation_id]
    text = get_message_by_name_for_user(name="wait_for_posts", telegram_id=user_id).text
    done = get_message_by_name_for_user(name="all_posts_loaded").text
    await message.delete()
    wait_mes = await mw.try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        keyboard=None,
        main_message_id=main_message_id,
        state=state
    )

    comp_mes_id = await send_compilation(compilation_id=compilation_id, chat_id=user_id, message=message,
                                         keyboard=await ik.get_compilations_menu(callback_data=callback_data,
                                                                                 post_id=compilation_id, is_in=True))
    delete_messages_list.append(comp_mes_id)
    posts = get_formatted_user_settings_posts_by_compilation_id(
        compilation_id=compilation_id,
        telegram_id=user_id
    )
    for post in posts:
        print(post)
        text = post[0]
        media = post[1][0]
        post_pk = post[2]
        media_type: int = media[0]
        media_path = media[1]
        mes_id = await mw.try_send_post_to_user(
            file_path=media_path,
            file_type=media_type,
            chat_id=user_id,
            text=text,
            message=message,
            keyboard=await ik.get_post_menu(callback_data=callback_data, post_id=post_pk, is_in=True)
        )
        delete_messages_list.append(mes_id)
        send_post_pk_list.append(post_pk)
    done_mes = await mw.try_send_message(
        message=message,
        user_id=user_id,
        text=done,
        keyboard=None,
        state=state
    )
    delete_messages_list.append(done_mes)
    await state.update_data(delete_messages_list=delete_messages_list,
                            send_compilation_list=send_compilation_list,
                            send_post_pk_list=send_post_pk_list,
                            compilation_id=compilation_id)


async def send_compilation(compilation_id: int, chat_id: int, message: types.Message, keyboard):
    compilation = get_compilation_by_id(compilation_id=compilation_id)
    compilation_file = compilation.contents.first()
    compilation_file_type = compilation_file.type
    mes_id = await mw.try_send_post_to_user(
        file_path=compilation_file.file.path,
        file_type=compilation_file_type,
        chat_id=chat_id,
        text=f"{compilation}\n{compilation.text}",
        message=message,
        keyboard=keyboard
    )
    return mes_id


async def edit_is_send_post(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    user_id = call.message.chat.id
    new_send_status = callback_data["status"] == "True"
    obj_id, compilation = int(callback_data["post_id"]), int(callback_data["comp_or_post"])
    if compilation:
        send_compilation_list = data.get("send_compilation_list")
        if int(obj_id) in send_compilation_list:
            send_compilation_list.remove(int(obj_id))
        else:
            send_compilation_list.append(int(obj_id))
        keyboard = await ik.get_compilations_menu(
            callback_data=callback_data,
            is_in=new_send_status,
            post_id=obj_id
        )
        await state.update_data(send_compilation_list=send_compilation_list)
    else:
        send_post_pk_list = data.get("send_post_pk_list")
        if int(obj_id) in send_post_pk_list:
            send_post_pk_list.remove(int(obj_id))
        else:
            send_post_pk_list.append(int(obj_id))
        keyboard = await ik.get_post_menu(
            callback_data=callback_data,
            is_in=new_send_status,
            post_id=obj_id
        )
        await state.update_data(send_post_pk_list=send_post_pk_list)

    await mw.try_edit_keyboard(
        chat_id=user_id,
        message_id=call.message.message_id,
        keyboard=keyboard
    )


async def select_platform(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    user_id = call.message.chat.id
    message_id = call.message.message_id
    text = get_message_by_name_for_user(name="select_platform", telegram_id=user_id).text
    keyboard = await ik.select_platform_menu(callback_data=callback_data)
    await mw.try_edit_message_caption(
        chat_id=user_id,
        text=text,
        message_id=message_id,
        keyboard=keyboard
    )


async def get_post_or_compilation(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    user_id = call.message.chat.id
    compilation = int(callback_data["comp_or_post"])
    obj_id = int(callback_data["post_id"])
    if compilation:
        compilation = get_compilation_by_id(compilation_id=obj_id)
        text = compilation.text
        keyboard = await ik.get_compilations_menu(
            callback_data=callback_data,
            is_in=obj_id in data.get("send_compilation_list"),
            post_id=obj_id
        )
    else:
        posts = get_formatted_user_settings_posts_by_compilation_id(compilation_id=data.get("compilation_id"),
                                                                    telegram_id=user_id, )
        text = "ERROR"
        for post in posts:
            if post[-1] == obj_id:
                text = post[0]
                break
        keyboard = await ik.get_post_menu(
            callback_data=callback_data,
            is_in=obj_id in data.get("send_post_pk_list"),
            post_id=obj_id
        )
    await mw.try_edit_message_caption(
        chat_id=user_id,
        text=text,
        message_id=call.message.message_id,
        keyboard=keyboard
    )


async def select_channel(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    user_id = call.message.chat.id
    text = get_message_by_name_for_user(name="select_channel", telegram_id=user_id).text
    keyboard = await ik.select_channel(
        callback_data=callback_data,
        user_id=user_id
    )
    await mw.try_edit_message_caption(
        chat_id=user_id,
        text=text,
        message_id=call.message.message_id,
        keyboard=keyboard
    )


async def change_post(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    user_id = call.message.chat.id
    message_id = call.message.message_id
    pinned_message = data.get("pinned_message", False)
    await call.answer(
        text=get_message_by_name_for_user(name="get_new_post_text", telegram_id=user_id).text,
        show_alert=True
    )
    await mw.try_edit_keyboard(
        chat_id=user_id,
        message_id=message_id,
        keyboard=None
    )
    if pinned_message:
        await mw.try_pin_unpin_message(
            chat_id=user_id,
            message_id=int(pinned_message),
            pin=False
        )
    await mw.try_pin_unpin_message(
        chat_id=user_id,
        message_id=message_id,
        pin=True
    )
    await state.update_data(pinned_message=message_id, callback_data=callback_data)
    await PostStates.GET_TEXT.set()


async def keep_updated_post(message: types.Message, state: FSMContext):
    data = await state.get_data()
    callback_data = data.get("callback_data")
    user_id = message.chat.id
    if "text" in message:
        add_user_post(
            post_id=int(callback_data["post_id"]),
            text=message.text,
            telegram_id=user_id
        )
        await mw.try_edit_message_caption(
            text=message.text,
            chat_id=user_id,
            message_id=data.get("pinned_message"),
            keyboard=await ik.get_post_menu(
                callback_data=callback_data,
                is_in=True,
                post_id=int(callback_data["post_id"])
            )
        )
        await MainMenu.MAIN_MENU.set()
    await message.delete()