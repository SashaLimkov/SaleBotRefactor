from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from bot.states.MainMenu import MainMenu
from bot.states.Signature import Signature
from bot.utils import message_worker as mw
from apps.settings.services.settings_user import update_field_settings, get_settings
from bot.keyboards import inline as ik


async def user_signature_menu(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["third_lvl"])
    if user_action == 0:
        await Signature.GET_SIGNATURE.set()
        await state.update_data(callback_data=callback_data)
        text = get_message_by_name_for_user(
            name="enter_signature", telegram_id=user_id
        ).text
        keyboard = await ik.cancel_signature_editing(callback_data=callback_data)
    else:
        update_field_settings(telegram_id=user_id, field="signature", value="")
        user_settings = get_settings(user_id)
        user_signature = user_settings.signature
        text_db = get_message_by_name_for_user(
            name="user_signature", telegram_id=user_id
        ).text
        text = (
            text_db.format(signature=user_signature)
            if user_signature
            else "Подпись отсутствует."
        )
        keyboard = await ik.get_signature_menu(
            callback_data=callback_data, user_signature=user_signature
        )

    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def set_user_signature(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await MainMenu.MAIN_MENU.set()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    signature = message.parse_entities()
    callback_data = data.get("callback_data")
    update_field_settings(telegram_id=user_id, field="signature", value=signature)
    user_settings = get_settings(user_id)
    user_signature = user_settings.signature
    text_db = get_message_by_name_for_user(
        name="user_signature", telegram_id=user_id
    ).text
    text = (
        text_db.format(signature=user_signature)
        if user_signature
        else "Подпись отсутствует."
    )
    keyboard = await ik.get_signature_menu(
        callback_data=callback_data, user_signature=user_signature
    )
    await message.delete()
    await mw.try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )
