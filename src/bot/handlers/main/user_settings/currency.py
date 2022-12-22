from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.settings.services.course import get_all_course_user, add_or_update_course_user
from apps.settings.services.settings_user import update_field_settings
from bot.states.Currency import Currency
from bot.states.MainMenu import MainMenu
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik
from bot.utils.validators import is_float_number


async def currency_settings(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["third_lvl"])
    if user_action in (0, 1):
        await update_selected_currency(
            user_action=user_action,
            user_id=user_id,
            call=call,
            main_message_id=main_message_id,
            callback_data=callback_data,
            state=state,
        )
    else:
        await select_currency_to_customize(
            call=call,
            callback_data=callback_data,
            state=state,
            main_message_id=main_message_id,
            user_id=user_id,
        )


async def update_selected_currency(
    user_action: int,
    user_id: int,
    call: types.CallbackQuery,
    main_message_id: int,
    callback_data: dict,
    state: FSMContext,
):
    custom_cur = await get_custom_currency_info(telegram_id=user_id)
    selected_cur = "RUB" if user_action else "Валюта сайта"
    text = get_message_by_name_for_user(
        name="currency_settings_main", telegram_id=user_id
    ).text.format(custom_cur=custom_cur, selected_cur=selected_cur)
    update_field_settings(telegram_id=user_id, field="currency", value=user_action)
    await call.answer(
        text="Вы установили валюту сайта."
        if not user_action
        else "Вы установили RUB валютой.",
        show_alert=True,
    )
    await mw.try_edit_message(
        text=text,
        message=call.message,
        user_id=user_id,
        main_message_id=main_message_id,
        keyboard=await ik.get_main_currency_settings_menu(callback_data=callback_data),
        state=state,
    )


async def select_currency_to_customize(
    call: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext,
    main_message_id: int,
    user_id: int,
):
    await MainMenu.MAIN_MENU.set()
    custom_cur = await get_custom_currency_info(telegram_id=user_id)
    text = get_message_by_name_for_user(
        name="select_currency_to_customize", telegram_id=user_id
    ).text.format(custom_cur=custom_cur)
    keyboard = await ik.get_custom_currency_menu(callback_data=callback_data)
    await mw.try_edit_message(
        text=text,
        user_id=user_id,
        message=call.message,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def press_currency_to_update(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    selected_cur = callback_data["selected_cur"]
    await state.update_data(callback_data=callback_data)
    await Currency.GET_CUR_VALUE.set()
    await mw.try_edit_message(
        message=call.message,
        main_message_id=main_message_id,
        user_id=user_id,
        text=get_message_by_name_for_user(
            name="write_cur_value", telegram_id=user_id
        ).text.format(selected_cur=selected_cur),
        keyboard=await ik.cancel_customize_selected_currency(
            callback_data=callback_data
        ),
        state=state,
    )


async def check_wrote_currency_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    value = message.text
    callback_data = data.get("callback_data")
    if await is_float_number(value):
        value = float(value.replace(",", "."))
        add_or_update_course_user(
            currency_name=callback_data["selected_cur"],
            telegram_id=user_id,
            value=float("%.2f" % value),
        )
        await MainMenu.MAIN_MENU.set()
        custom_cur = await get_custom_currency_info(telegram_id=user_id)
        text = get_message_by_name_for_user(
            name="select_currency_to_customize", telegram_id=user_id
        ).text.format(custom_cur=custom_cur)
        keyboard = await ik.get_custom_currency_menu(callback_data=callback_data)
    else:
        text = get_message_by_name_for_user(
            name="custom_curr_error", telegram_id=user_id
        ).text
        keyboard = await ik.cancel_customize_selected_currency(
            callback_data=callback_data
        )
    await message.delete()
    await mw.try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def get_custom_currency_info(telegram_id: int) -> str:
    custom_cur_list = get_all_course_user(telegram_id=telegram_id)
    text = ""
    for currency in custom_cur_list:
        text += f"{currency.currency.name} - {currency.value}\n"
    return text
