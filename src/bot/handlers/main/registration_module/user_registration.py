from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import deep_linking

from apps.message.services.message import get_message_by_name_for_user
from apps.profiles.services.profile import create_user
from apps.profiles.services.rate import get_rate_by_pk
from apps.profiles.services.subscription import get_user_active_subscription
from apps.settings.services.chanel import get_list_telegram_channels, add_channel_telegram
from apps.settings.services.deep_link import get_deep_link_by_identifier_and_tg_id, close_deep_link_identifier_and_tg_id
from bot.keyboards import inline as ik
from bot.keyboards import reply as rk
from bot.states.Registration import UserRegistration
from bot.utils import deleter
from bot.utils.message_worker import try_edit_message, try_send_message, try_send_video, send_confirmed_message


async def start_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    text = get_message_by_name_for_user(name="start_registration")
    args = message.get_args()
    if args:
        selected_sub_pk, inviter_id, identifier = deep_linking.decode_payload(args).split("_")
        await state.update_data(
            selected_sub_pk=selected_sub_pk,
            inviter_id=inviter_id,
            identifier=identifier
        )
    if main_message_id:
        await try_edit_message(
            message=message,
            user_id=user_id,
            text=text.text,
            main_message_id=main_message_id,
            keyboard=await ik.get_start_registration_keyboard(),
            state=state,
        )
    else:
        await try_send_message(
            message=message,
            user_id=user_id,
            text=text.text,
            keyboard=await ik.get_start_registration_keyboard(),
            state=state,
        )


async def get_main_registration_menu(call: types.CallbackQuery, state: FSMContext):
    await get_registration_menu(message=call.message, state=state)


async def get_registration_menu(message: types.Message, state: FSMContext):
    await UserRegistration.MENU.set()
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    text = get_message_by_name_for_user(name="registration_main_menu")
    fio = data.get("fio", False)
    phone = data.get("phone", False)
    text = text.text.format(
        name=message.chat.full_name,
        fio=fio if fio else "",
        phone=phone if phone else "",
    )
    if fio and phone:
        await try_edit_message(
            message=message,
            user_id=user_id,
            text=text,
            keyboard=await ik.get_user_registration_menu(done=True),
            main_message_id=main_message_id,
            state=state,
        )
        return
    await try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        keyboard=await ik.get_user_registration_menu(),
        main_message_id=main_message_id,
        state=state,
    )


async def press_user_fio_or_phone(
        call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.from_user.id
    if callback_data["action"] == "1":
        await UserRegistration.FIO.set()
        text = get_message_by_name_for_user(name="registration_get_fio").text
        await try_edit_message(
            message=call,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=0,
            state=state,
        )
    else:
        await UserRegistration.PHONE_NUMBER.set()
        text = get_message_by_name_for_user(name="registration_get_phone").text
        await try_edit_message(
            message=call,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=await rk.get_user_contact(),
            state=state,
        )


async def get_user_fio(message: types.Message, state: FSMContext):
    await state.update_data({"fio": message.text})
    await message.delete()
    await get_registration_menu(message=message, state=state)


async def get_user_phone(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.delete()
    await get_registration_menu(message=message, state=state)


async def confirm_data(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    fio = data.get("fio", False)
    phone = data.get("phone", False)
    first_name = call.message.chat.first_name
    text = get_message_by_name_for_user(name="confirm_registration").text.format(
        name=first_name
    )
    last_name = call.message.chat.last_name
    username = call.message.chat.username
    inviter_id = int(data.get("inviter_id", False))
    if inviter_id:
        identifier = int(data.get("identifier"))
        print(identifier, inviter_id)
        dl = get_deep_link_by_identifier_and_tg_id(identifier=identifier, tg_id=inviter_id)
        print(dl.used)
        if dl.used:
            await try_edit_message(
                message=call.message,
                user_id=user_id,
                text="Срок действия данной ссылки истек. Напишите /start и пройдите регистрацию заново",
                main_message_id=main_message_id,
                keyboard=None,
                state=state
            )
            return
        rate = get_rate_by_pk(rate_pk=int(data.get("selected_sub_pk"), 0))
        helper_days = get_user_active_subscription(telegram_id=inviter_id).days_left
        user = create_user(
            telegram_id=user_id,
            phone=phone,
            full_name=fio,
            first_name=first_name,
            last_name=last_name if last_name else "",
            username=username if username else "",
            helper_days=helper_days,
            rate=rate.name,
            cheque=rate.description,
            inviter_id=inviter_id,
            is_helper=True
        )
        inviter_channels = get_list_telegram_channels(telegram_id=inviter_id)
        for channel in inviter_channels:
            add_channel_telegram(user_id, channel.name, channel.chat_id)  # Нужно с вк тоже самое сделать
        close_deep_link_identifier_and_tg_id(identifier=identifier, tg_id=inviter_id)

    else:
        user = create_user(
            telegram_id=user_id,
            phone=phone,
            full_name=fio,
            first_name=first_name,
            last_name=last_name if last_name else "",
            username=username if username else "",
        )
    if user:
        await deleter.try_delete_message(chat_id=user_id, message_id=main_message_id)
        await try_send_video(
            video_path="bot/media/hello.mp4",
            chat_id=user_id,
            text="",
            message=call.message,
            state=state,
            keyboard=None,
            splited_message=True,
        )
        await send_confirmed_message(chat_id=user_id, text=text)
        await try_send_message(
            message=call.message,
            user_id=user_id,
            text=get_message_by_name_for_user("main_menu_message").text,
            keyboard=await ik.get_main_menu(user.in_chat),
            state=state
        )
