from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.settings.services.settings_user import get_settings, update_field_settings
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw


async def link_settings_menu(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    field = callback_data["third_lvl"]
    settings = get_settings(telegram_id=user_id)
    data_dict = {
        "link": settings.link,
        "hided_link": settings.hided_link,
    }
    callback = {
        "link": "Короткая ссылка",
        "hided_link": "Ссылка в тексте",
    }
    update_field_settings(
        telegram_id=user_id,
        field=field,
        value=not data_dict[field]
    )
    await call.answer(
        text=f"Поле {callback[field]} {'отключено.' if data_dict[field] else 'включено.'}"
    )
    text = get_message_by_name_for_user(name="link_settings", telegram_id=user_id).text
    keyboard = await ik.get_link_settings_menu(callback_data=callback_data, telegram_id=user_id)
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )
