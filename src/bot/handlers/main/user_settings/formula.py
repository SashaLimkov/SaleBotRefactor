from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.message.services.message import get_message_by_name_for_user
from apps.settings.services.settings_user import update_field_settings, get_settings
from bot.keyboards import inline as ik
from bot.states.Commission import Commission
from bot.states.MainMenu import MainMenu
from bot.utils import message_worker as mw
from bot.utils.validators import is_float_number


async def formula_and_commission_menu(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    user_action = int(callback_data["third_lvl"])
    user_settings = get_settings(telegram_id=user_id)
    if user_action == 0:
        call_text = "Вы выбрали формулу без комиссии."
        await call.answer(text=call_text, show_alert=True)
        if user_settings.formula == 0:
            return
        update_field_settings(telegram_id=user_id, field="formula", value=0)
        text, selected_formula = await get_formula_commission_text_and_selected_formula(
            user_id=user_id
        )
        keyboard = await ik.get_formula_commission(
            callback_data=callback_data, selected_formula=selected_formula
        )
    elif user_action == 1:
        call_text = "Вы выбрали формулу с комиссией"
        await call.answer(text=call_text, show_alert=True)
        if user_settings.formula == 1:
            return
        update_field_settings(telegram_id=user_id, field="formula", value=1)
        text, selected_formula = await get_formula_commission_text_and_selected_formula(
            user_id=user_id
        )
        keyboard = await ik.get_formula_commission(
            callback_data=callback_data, selected_formula=selected_formula
        )
    else:
        text = get_message_by_name_for_user(
            name="enter_commission", telegram_id=user_id
        ).text
        keyboard = await ik.cancel_commission_editing(callback_data=callback_data)
        await state.update_data(callback_data=callback_data)
        await Commission.GET_COMMISSION.set()
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def check_commission(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    value = message.text
    callback_data = data.get("callback_data")
    if await is_float_number(value):
        value = float(value.replace(",", "."))
        update_field_settings(
            telegram_id=user_id, field="commission", value=float("%.2f" % value)
        )
        await MainMenu.MAIN_MENU.set()
        text, selected_formula = await get_formula_commission_text_and_selected_formula(
            user_id=user_id
        )
        keyboard = await ik.get_formula_commission(
            callback_data=callback_data, selected_formula=selected_formula
        )
    else:
        text = get_message_by_name_for_user(
            name="custom_curr_error", telegram_id=user_id
        ).text
        keyboard = await ik.cancel_commission_editing(callback_data=callback_data)
    await message.delete()
    await mw.try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        keyboard=keyboard,
        state=state,
    )


async def get_formula_commission_text_and_selected_formula(user_id: int) -> tuple:
    user_settings = get_settings(telegram_id=user_id)
    selected_formula = user_settings.formula
    commission = user_settings.commission
    commission_text = f"Размер комиссии: {commission}%" if selected_formula else ""
    text = get_message_by_name_for_user(
        name="formula_with_or_without_comission", telegram_id=user_id
    ).text.format(
        selected_formula="Без комиссии" if not selected_formula else "С комиссией",
        commission=commission_text,
    )
    return text, selected_formula
