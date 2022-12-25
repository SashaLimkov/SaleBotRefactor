from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_list_helpers_profile
from apps.profiles.services.rate import get_rate_by_pk, get_helper_rate_by_price
from apps.profiles.services.subscription import create_user_subscription, get_user_active_subscription
from bot.config import bot
from bot.handlers.main.subscriptions.helper_sub import success_sub_helper
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik
from core import settings
from core.settings import CHANNEL


async def create_invoice_to_rate(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    selected_sub_pk = int(callback_data["rate_pk"])
    rate = get_rate_by_pk(rate_pk=selected_sub_pk)
    keyboard = await ik.cancel_invoice(callback_data=callback_data)
    await state.update_data(callback_data=callback_data)
    price = 0
    if user_id in [390959255, 590664623]:
        price = 50
    amount = int(rate.price) * 100 if not price else price * 100
    description = f'Оплата тарифа: {rate.name} для {user_id}'
    helpers = get_list_helpers_profile(telegram_id=user_id)
    items = [
        {
            "name": f"Тариф: {rate.name} для {call.message.chat.id}",
            "quantity": 1,
            "sum": rate.price if not price else price,
            "payment_method": "full_payment",
            "tax": "none"
        }]
    if helpers:
        price = int(rate.price) * 100 if not price else price * 100
        helpers_tax = price // 10
        helpers_count = len(helpers)
        description = f'Оплата тарифа: {rate.name} для {user_id}, с учётом помощников пользователя ({helpers_count}).'
        amount = price + helpers_tax
        items.append(
            {
                "name": f"Тариф: {rate.name} для помощников {call.message.chat.id}",
                "quantity": helpers_count,
                "sum": helpers_tax // 100,
                "payment_method": "full_payment",
                "tax": "none"
            }
        )
        await state.update_data(helpers_tax=helpers_tax // 100)

    await mw.try_send_invoice(
        message=call.message,
        user_id=user_id,
        keyboard=keyboard,
        state=state,
        main_message_id=main_message_id,
        title=f'Оплата тарифа: {rate.name}',
        description=description,
        payload='payment',
        currency='RUB',
        prices=[{'label': 'Руб', 'amount': amount}],
        provider_token='1902332405:LIVE:638036107957339291',
        provider_data={
            "Receipt": {
                "items": items}}
    )


async def check_payment(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, True)


async def oplata_ok(message: types.SuccessfulPayment, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    callback_data = data.get("callback_data")
    helpers_tax = data.get("helpers_tax", False)
    amount = message.successful_payment.total_amount / 100
    user_id = message.chat.id
    if user_id in [390959255, 590664623]:
        rate = get_helper_rate_by_price(price=200000 / 100)
    else:
        rate = get_helper_rate_by_price(price=amount - helpers_tax if helpers_tax else amount)

    if "inviter_id" in callback_data:
        await success_sub_helper(user_id=user_id,
                                 message=message,
                                 callback_data=callback_data,
                                 state=state)
    else:
        user_rate = get_user_active_subscription(telegram_id=user_id)
        create_user_subscription(
            telegram_id=user_id,
            cheque=rate.description,
            rate=rate.name,
            active=True if user_rate is None else False,
        )
        user_rate = get_user_active_subscription(telegram_id=user_id)
        expire_date = datetime.now() + timedelta(days=user_rate.days_left)
        await bot.unban_chat_member(chat_id=settings.CHANNEL, user_id=user_id, only_if_banned=True)
        link = await bot.create_chat_invite_link(chat_id=settings.CHANNEL, member_limit=1, expire_date=expire_date)
        await mw.try_edit_message(
            message=message,
            user_id=user_id,
            text=get_message_by_name_for_user(telegram_id=user_id, name="payment_done").text.format(
                link=link.invite_link),
            main_message_id=main_message_id,
            keyboard=await ik.cancel_invoice(callback_data=callback_data),
            state=state,
        )
    text = f"Новая продажа подписки на {rate.count_day_sub} дней за {amount} рублей.\n" \
           f"Покупатель: {message.chat.id}\n" \
           f"Никнейм: {'@' + message.chat.username if message.chat.username else 'Отсутствует'}"
    await mw.try_send_message(
        message=message,
        user_id=878849282,
        text=text,
        keyboard=None,
        state=state
    )
    await mw.try_send_message(
        message=message,
        user_id=390959255,
        text=text,
        keyboard=None,
        state=state
    )
