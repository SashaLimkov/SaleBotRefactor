from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.profiles.services.rate import get_rate_by_pk
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik


async def create_invoice_to_rate(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    selected_sub_pk = int(callback_data["rate_pk"])
    rate = get_rate_by_pk(rate_pk=selected_sub_pk)
    keyboard = await ik.cancel_invoice(callback_data=callback_data)
    await mw.try_send_invoice(
        message=call.message,
        user_id=user_id,
        keyboard=keyboard,
        state=state,
        main_message_id=main_message_id,
        title=f'Оплата тарифа: {rate.name}',
        description=f'Оплата тарифа: {rate.name} для {call.message.chat.id}',
        payload='payment',
        currency='RUB',
        prices=[{'label': 'Руб', 'amount': int(rate.price) * 100}],
        provider_token='1902332405:LIVE:638036107957339291',
        provider_data={
            "Receipt": {
                "items": [
                    {
                        "name": f"Тариф: {rate.name} для {call.message.chat.id}",
                        "quantity": 1,
                        "sum": rate.price,
                        "payment_method": "full_payment",
                        "tax": "none"
                    }]}}
    )
