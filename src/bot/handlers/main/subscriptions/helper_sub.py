import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import deep_linking
from aiogram.utils.markdown import hcode

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.rate import get_rate_by_pk
from apps.profiles.services.subscription import get_user_active_subscription
from apps.settings.services.deep_link import create_deep_link
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik


async def buy_sub_to_helper(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    selected_sub_pk = int(callback_data["rate_pk"])
    text = get_message_by_name_for_user(name="rate_info", telegram_id=user_id).text
    inviter_sub_days = get_user_active_subscription(telegram_id=user_id).days_left
    rate = get_rate_by_pk(rate_pk=selected_sub_pk)
    text = text.format(
        rate_name=rate.name,
        price=rate.price,
        sign=rate.currency,
        count_days=inviter_sub_days,
        description=rate.description.format(days=inviter_sub_days)
    )
    keyboard = await ik.get_pay_or_cancel_menu_helper(callback_data=callback_data)
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        keyboard=keyboard,
        main_message_id=main_message_id,
        state=state
    )


async def success_sub_helper(user_id, message, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    selected_sub_pk = int(callback_data["rate_pk"])
    inviter_id = int(callback_data["inviter_id"])
    identifier = random.randint(999999, 99999999)
    share_link = await deep_linking.get_start_link(
        f"{selected_sub_pk}_{inviter_id}_{identifier}", encode=True
    )
    dl = create_deep_link(telegram_id=user_id, deep_link=share_link, identifier=identifier)
    text = get_message_by_name_for_user(
        name="success_helper_sub_buy",
        telegram_id=user_id).text.format(deep_link=hcode(share_link))
    keyboard = await ik.back_to_main_menu(callback_data=callback_data)
    await mw.send_confirmed_message(chat_id=user_id, text=text)
    await mw.try_send_message(
        message=message,
        user_id=user_id,
        text="Вернуться в главное меню",
        keyboard=keyboard,
        state=state
    )
