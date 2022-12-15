from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.settings.services.settings_user import get_settings, update_field_settings
from bot.keyboards import inline as ik
from bot.states.LogoAndTLogo import LogoAndTLogo
from bot.states.MainMenu import MainMenu
from bot.utils import message_worker as mw


async def logo_and_t_logo_settings(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["third_lvl"])
    await state.update_data(callback_data=callback_data)
    if user_action:
        await LogoAndTLogo.EDIT_TEXT_LOGO.set()
        text = get_message_by_name_for_user(name="enter_t_logo", telegram_id=user_id).text
        keyboard = await ik.cancel_updating_logo_or_t_logo(callback_data=callback_data)
    else:
        pass
    await mw.try_edit_message(
        message=call.message,
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
    t_logo = message.text  # нужна защита от говна (если не будет текста)
    callback_data = data.get("callback_data")
    update_field_settings(
        telegram_id=user_id,
        field="text_logo",
        value=t_logo
    )
    text = get_message_by_name_for_user(name="text_logo_settings", telegram_id=user_id).text.format(
        t_logo=t_logo
    )
    keyboard = await ik.logo_settings(callback_data=callback_data, telegram_id=user_id)
    await message.delete()
    await MainMenu.MAIN_MENU.set()
    await mw.try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def set_logo_or_t_logo_position(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    position = callback_data["third_lvl"]
    print(position)
    if position in ("center", "fill"):
        update_field_settings(
            telegram_id=user_id,
            field="logo_position",
            value=position
        )
    elif position == "off":
        update_field_settings(
            telegram_id=user_id,
            field="logo_position",
            value=""
        )
    else:
        update_field_settings(
            telegram_id=user_id,
            field="logo_position",
            value=None
        )
        update_field_settings(
            telegram_id=user_id,
            field="text_logo",
            value=None
        )
        # update_field_settings( Нужен запрос на удаление фото, даже если его нет.
        #     telegram_id=user_id,
        #     field="logo",
        #     value=""
        # )
    user_settings = get_settings(telegram_id=user_id)
    logo = user_settings.logo
    text_logo = user_settings.text_logo
    if not text_logo and not logo:
        text = get_message_by_name_for_user(name="select_wm_action", telegram_id=user_id).text
        keyboard = await ik.get_wm_add_logo_menu(callback_data=callback_data)
    elif text_logo:
        text = get_message_by_name_for_user(name="text_logo_settings", telegram_id=user_id).text.format(
            t_logo=text_logo
        )
        keyboard = await ik.logo_settings(callback_data=callback_data, telegram_id=user_id)
    elif logo:
        text = get_message_by_name_for_user(name="photo_logo_settings", telegram_id=user_id).text
        keyboard = await ik.logo_settings(callback_data=callback_data, telegram_id=user_id)
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )
