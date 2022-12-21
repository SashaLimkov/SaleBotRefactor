import datetime
import hashlib

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from apps.message.services.message import get_message_by_name_for_user
from apps.posts.services.compilation import get_list_compilations_by_date
from bot.utils import message_worker as mw
from bot.keyboards import inline as ik
from bot.utils.deleter import try_delete_message


async def show_compilations_by_date_call(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    user_id = call.message.chat.id
    await state.update_data(callback_data=callback_data)
    await cleaner(state=state, user_id=user_id)
    text = get_message_by_name_for_user(name="date_selected", telegram_id=user_id).text
    keyboard = await ik.get_select_compilation_menu(callback_data=callback_data)
    await mw.try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=call.message.message_id,
        keyboard=keyboard,
        state=state
    )


async def inline_compilations(inline_query: types.InlineQuery, state: FSMContext):
    data = await state.get_data()
    callback_data = data.get("callback_data")
    results = []
    date = datetime.datetime.strptime(callback_data["date"], "%Y-%m-%d")
    compilations_list = get_list_compilations_by_date(date=date)
    if compilations_list:
        for index, compilation in enumerate(compilations_list):
            if compilation.message_id:
                result_id: str = hashlib.md5(str(index).encode()).hexdigest()
                results.append(
                    InlineQueryResultArticle(
                        id=result_id,
                        title=f"{'✅' if compilation.done else '⏳'} {compilation.date} | {compilation.name}",
                        input_message_content=InputTextMessageContent(
                            f"{compilation.name}|:|{compilation.pk}"
                        ),
                    )
                )
    switch_text = "Выбрать дату релиза >>"
    return await inline_query.answer(
        results,
        cache_time=0,
        is_personal=True,
        switch_pm_parameter="select_section",
        switch_pm_text=switch_text,
    )


async def cleaner(state: FSMContext, user_id: int):
    data = await state.get_data()
    pinned_message = data.get("pinned_message", False)
    if pinned_message:
        await mw.try_pin_unpin_message(
            chat_id=user_id,
            message_id=int(pinned_message),
            pin=False
        )
    mes_id_list = data.get("delete_messages_list", False)
    if mes_id_list:
        await try_delete_message(chat_id=user_id, message_id=mes_id_list)
        await state.update_data(delete_messages_list=[])
