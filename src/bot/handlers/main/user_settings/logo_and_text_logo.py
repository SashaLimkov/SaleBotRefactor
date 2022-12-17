import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.settings.services.settings_user import get_settings, update_field_settings
from bot.keyboards import inline as ik
from bot.states.LogoAndTLogo import LogoAndTLogo
from bot.states.MainMenu import MainMenu
from bot.utils import message_worker as mw


async def logo_and_t_logo_settings(
        call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["third_lvl"])
    await state.update_data(callback_data=callback_data)
    if user_action:
        await LogoAndTLogo.EDIT_TEXT_LOGO.set()
        text = get_message_by_name_for_user(
            name="enter_t_logo", telegram_id=user_id
        ).text
    else:
        await LogoAndTLogo.EDIT_LOGO.set()
        text = get_message_by_name_for_user(
            name="enter_logo", telegram_id=user_id
        ).text
    keyboard = await ik.cancel_updating_logo_or_t_logo(callback_data=callback_data)
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def set_logo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    callback_data = data.get("callback_data")
    await message.delete()
    if "document" in message:
        document = message.document
        file_type = document.file_name.split(".")[-1]
        await message.document.download(
            destination_file=f"photos/{user_id}.{file_type}"
        )
        update_field_settings(
            telegram_id=user_id,
            field="logo",
            value=f"photos/{user_id}.{file_type}"
        )
        os.remove(path=f"photos/{user_id}.{file_type}")
        text = get_message_by_name_for_user(
            name="logo_settings", telegram_id=user_id
        ).text
        keyboard = await ik.logo_settings(callback_data=callback_data, telegram_id=user_id)
        await MainMenu.MAIN_MENU.set()
        user_settings = get_settings(telegram_id=user_id)
        await mw.try_edit_photo(
            photo_path=user_settings.logo.path,
            chat_id=user_id,
            text=text,
            keyboard=keyboard,
            main_message_id=main_message_id,
            state=state,
            message=message
        )
    else:
        text = get_message_by_name_for_user(
            name="logo_error", telegram_id=user_id
        ).text
        keyboard = await ik.cancel_updating_logo_or_t_logo(callback_data=callback_data)
        await mw.try_edit_message(
            message=message,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=keyboard,
            state=state,
        )


async def set_t_logo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    callback_data = data.get("callback_data")
    await message.delete()
    if "text" in message:
        t_logo = message.text  # нужна защита от говна (если не будет текста)
        update_field_settings(telegram_id=user_id, field="text_logo", value=t_logo)
        text = get_message_by_name_for_user(
            name="text_logo_settings", telegram_id=user_id
        ).text.format(t_logo=t_logo)
        keyboard = await ik.logo_settings(callback_data=callback_data, telegram_id=user_id)
        await MainMenu.MAIN_MENU.set()
    else:
        text = get_message_by_name_for_user(
            name="text_logo_error", telegram_id=user_id
        ).text
        keyboard = await ik.cancel_updating_logo_or_t_logo(callback_data=callback_data)

    await mw.try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def set_logo_or_t_logo_position(
        call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    position = callback_data["third_lvl"]
    if position in ("center", "fill"):
        update_field_settings(
            telegram_id=user_id, field="logo_position", value=position
        )
    elif position == "off":
        update_field_settings(telegram_id=user_id, field="logo_position", value="")
    else:
        update_field_settings(telegram_id=user_id, field="logo_position", value=None)
        update_field_settings(telegram_id=user_id, field="text_logo", value=None)
        update_field_settings(
            telegram_id=user_id,
            field="logo",
            value=None
        )
    user_settings = get_settings(telegram_id=user_id)
    text, keyboard, photo = await return_text_and_keyboard_for_wm_settings(
        user_settings=user_settings, user_id=user_id, callback_data=callback_data
    )
    if photo:
        await mw.try_edit_photo(
            photo_path=user_settings.logo.path,
            chat_id=user_id,
            text=text,
            message=call.message,
            main_message_id=main_message_id,
            state=state,
            keyboard=keyboard
        )
    else:
        await mw.try_edit_message(
            message=call.message,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=keyboard,
            state=state,
        )


async def return_text_and_keyboard_for_wm_settings(
        user_settings, user_id: int, callback_data: dict
):
    logo = user_settings.logo
    text_logo = user_settings.text_logo
    photo = False
    if not text_logo and not logo:
        text = get_message_by_name_for_user(
            name="select_wm_action", telegram_id=user_id
        ).text
        keyboard = await ik.get_wm_add_logo_menu(callback_data=callback_data)
    elif text_logo:
        text = get_message_by_name_for_user(
            name="text_logo_settings", telegram_id=user_id
        ).text.format(t_logo=text_logo)
        keyboard = await ik.logo_settings(
            callback_data=callback_data, telegram_id=user_id
        )
    else:
        text = get_message_by_name_for_user(
            name="logo_settings", telegram_id=user_id
        ).text
        keyboard = await ik.logo_settings(
            callback_data=callback_data, telegram_id=user_id
        )
        photo = True

    return text, keyboard, photo
