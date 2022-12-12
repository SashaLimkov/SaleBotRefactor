from bot.utils.datetime_helper import get_datetime
from bot.utils.keyboard_utils.base_keyboard_utils import get_base_keyboard
from bot.data import callback_data as cd
from bot.data import list_and_tuple_data as ld

__all__ = [
    "get_main_menu",
    "get_settings_menu",
    "get_date_menu",
    "get_sub_menu",
    "get_video_menu",
]


async def get_main_menu(in_chat):
    buttons = [
        {"text": value, "callback_data": cd.mm.new(action=index + 1)}
        for index, value in enumerate(ld.MAIN_MENU)
    ]
    buttons += [
        {"text": "🎦Видео-инструкция", "callback_data": cd.mm.new(action=4)},
        {"text": "👩‍💻 поддержка бота", "url": "https://t.me/deva_v_brendax"},
    ]

    if not in_chat:
        buttons.append(
            {"text": "👉 Доступ в канал 👈", "callback_data": cd.ADD_TO_CHANNEL}
        )
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 2,
        },
    )


async def get_settings_menu(callback_data: dict):
    buttons = [
        {
            "text": value,
            "callback_data": cd.settings_menu.new(
                first_lvl=callback_data["action"], second_lvl=index + 1
            ),
        }
        for index, value in enumerate(ld.SETTINGS_MENU)
    ]
    buttons.append({"text": "◀ Назад", "callback_data": cd.MAIN_MENU})
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 1,
        },
    )


async def get_date_menu():
    three_days_before_today = str(await get_datetime("3t")).split(" ")[0]
    the_day_before_yesterday = str(await get_datetime("2t")).split(" ")[0]
    yesterday = str(await get_datetime("yt")).split(" ")[0]
    today = str(await get_datetime("td")).split(" ")[0]
    days = (three_days_before_today, the_day_before_yesterday, yesterday, today)
    buttons = [{"text": day, "callback_data": f"day_{day}"} for day in days]
    buttons.append({"text": "◀ Назад", "callback_data": cd.MAIN_MENU})
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 1,
        },
    )


async def get_sub_menu(is_active: bool, is_helper: bool, callback_data: dict):
    buttons = []
    if is_active and not is_helper:
        buttons = [
            {
                "text": value,
                "callback_data": cd.sub_menu.new(
                    first_lvl=callback_data["action"], second_lvl=index + 1
                ),
            }
            for index, value in enumerate(ld.SUBSCRIPTION_MENU)
        ]
    buttons.append({"text": "◀ Назад", "callback_data": cd.MAIN_MENU})
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 1,
        },
    )


async def get_video_menu():
    buttons = [
        {"text": "◀ Назад", "callback_data": cd.MAIN_MENU},
    ]
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 1,
        },
    )
