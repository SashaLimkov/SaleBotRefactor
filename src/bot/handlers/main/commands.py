from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import get_profile_by_telegram_id, get_all_profiles
from apps.profiles.services.subscription import get_user_active_subscription
from bot.config import bot
from bot.handlers.main.posts.date_and_inline import cleaner
from bot.states.MainMenu import MainMenu
from bot.utils.deleter import try_delete_message
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik
from bot.utils.message_worker import kick_user


async def start_command(message: types.Message, state: FSMContext):
    await MainMenu.MAIN_MENU.set()
    data = await state.get_data()
    user_id = message.chat.id
    await cleaner(state=state, user_id=user_id)
    user = get_profile_by_telegram_id(telegram_id=user_id)
    text = get_message_by_name_for_user(
        name="main_menu_message", telegram_id=user_id
    ).text.format(name=user.first_name)
    await message.delete()
    await mw.try_send_message(
        user_id=user_id,
        text=text,
        message=message,
        state=state,
        keyboard=await ik.get_main_menu(user.in_chat, user.is_helper, user.telegram_id),
    )


async def anons(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    callback_data = data.get("callback_data")
    text = get_message_by_name_for_user(
        name="select_date", telegram_id=user_id
    ).text
    keyboard = await ik.get_date_menu(callback_data=callback_data)
    await try_delete_message(
        chat_id=user_id,
        message_id=message.message_id
    )
    await mw.try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        keyboard=keyboard,
        main_message_id=main_message_id,
        state=state
    )


async def fix_users(message: types.Message, state: FSMContext):
    profiles = get_all_profiles()
    for profile in profiles:
        sub = get_user_active_subscription(telegram_id=profile.telegram_id)
#         if sub:
#             if sub.days_left < 0:
#                 await kick_user(chat_id=profile.telegram_id)
#                 sub.days_left = 0
#                 sub.active = False
#                 sub.save()
#             days_from_buy = datetime.today() - sub.datetime_buy
#             fixed_days = sub.days_left - days_from_buy.days
#             if fixed_days < 0:
#                 await kick_user(chat_id=profile.telegram_id)
#                 sub.days_left = 0
#                 sub.active = False
#                 sub.save()
#                 await mw.try_send_message(
#                     message=message,
#                     user_id=profile.telegram_id,
#                     text=f"""{abs(fixed_days)} дней назад у вас кончилась подписка.
# После оплаты новой подписки у вас вычтется {abs(fixed_days)} дней. Напишите /start""",
#                     keyboard=None,
#                     state=state
#                 )
#             print(f'Дата покупки {sub.datetime_buy}\n'
#                   f'Пользователь {profile.telegram_id}\n'
#                   f'Количество дней по админке {sub.days_left}\n'
#                   f'Прошло со дня покупки {days_from_buy.days}\n'
#                   f'Количество дней должно быть {fixed_days}\n'
#                   f'________________________________________________________________________')
            # sub.days_left = fixed_days
            # if fixed_days == 0:
            #     sub.active = False
            # sub.save()

    await mw.try_send_message(
        message=message,
        user_id=message.chat.id,
        text=f"{len(profiles)}",
        state=state,
        keyboard=None,
    )
