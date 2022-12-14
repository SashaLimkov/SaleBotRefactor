from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.settings.services.settings_product_user import get_product_settings, update_field_product_settings
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw


async def product_settings_menu(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    field = callback_data["third_lvl"]
    settings = get_product_settings(telegram_id=user_id)
    data_dict = {
        "link": settings.link,
        "name": settings.name,
        "price": settings.price,
        "discount": settings.discount,
        "sizes": settings.sizes,
        "description": settings.description
    }
    callback = {
        "link": "Ссылка",
        "name": "Название",
        "price": "Цена",
        "discount": "Скидка",
        "sizes": "Размеры",
        "description": "Описание",
    }
    update_field_product_settings(
        telegram_id=user_id,
        field=field,
        value=not data_dict[field]
    )
    await call.answer(
        text=f"Поле {callback[field]} {'отключено.' if data_dict[field] else 'включено.'}"
    )
    text = get_message_by_name_for_user(name="product_settings", telegram_id=user_id).text
    keyboard = await ik.get_product_settings_menu(callback_data=callback_data, telegram_id=user_id)
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )
