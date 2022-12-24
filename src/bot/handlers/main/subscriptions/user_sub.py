from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_is_helper
from apps.profiles.services.rate import get_rate_by_pk
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik


async def select_sub_to_buy(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    selected_sub_pk = int(callback_data["third_lvl"])
    text = get_message_by_name_for_user(name="rate_info", telegram_id=user_id).text
    rate = get_rate_by_pk(rate_pk=selected_sub_pk)
    text = text.format(
        rate_name=rate.name,
        price=rate.price,
        sign=rate.currency,
        count_days=rate.count_day_sub,
        description=rate.description
    )
    keyboard = await ik.get_pay_or_cancel_menu(callback_data=callback_data)
    if get_profile_is_helper(user_id):
        text = get_message_by_name_for_user(name="helper_cant_buy_sub", telegram_id=user_id).text
        keyboard = await ik.back_to_main_menu(callback_data=callback_data)

    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        keyboard=keyboard,
        main_message_id=main_message_id,
        state=state
    )
