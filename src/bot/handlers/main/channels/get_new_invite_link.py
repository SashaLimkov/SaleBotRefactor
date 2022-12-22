from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.subscription import get_user_active_subscription
from bot.config import bot
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw


async def get_invite_link(
        call: types.CallbackQuery, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_rate = get_user_active_subscription(telegram_id=user_id)
    expire_date = datetime.now() + timedelta(days=user_rate.days_left)
    try:
        link = await bot.create_chat_invite_link(chat_id=-1001769191780, member_limit=1, expire_date=expire_date)
        link = link.invite_link
    except:
        link = "У вас кончилась подписка."
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=get_message_by_name_for_user(telegram_id=user_id, name="add_me_to_channel").text.format(
            link=link),
        main_message_id=main_message_id,
        keyboard=await ik.back_to_main_menu(),
        state=state,
    )
