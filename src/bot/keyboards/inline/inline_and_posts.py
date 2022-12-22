from apps.settings.services.chanel import get_list_telegram_channels
from apps.settings.services.settings_product_user import get_product_settings
from apps.settings.services.settings_user import get_settings
from bot.utils.keyboard_utils.base_keyboard_utils import (
    get_base_keyboard,
    get_inline_button,
)
from bot.data import callback_data as cd

__all__ = [
    "get_select_compilation_menu",
    "get_compilations_menu",
    "get_post_menu",
    "select_platform_menu",
    "select_channel",
]


async def get_select_compilation_menu(callback_data: dict):
    buttons = [
        {
            "text": "Выбрать подборку",
            "switch_inline_query_current_chat": "",
        },
        {
            "text": "◀ Назад",
            "callback_data": cd.mm.new(action=callback_data["action"])
        }
    ]
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 1,
        }
    )


async def get_compilations_menu(callback_data: dict, is_in: bool, post_id: int, comp_or_post=1):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    keyboard.add(
        await get_inline_button(
            text=f"{'✅' if not is_in else '❌'}Исключить пост из выгрузки",
            cd=cd.turn_on_or_off_post.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=comp_or_post,
                post_id=post_id,
                status=not is_in
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Отправить пост",
            cd=cd.send_one_or_all.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=comp_or_post,
                post_id=post_id,
                send_one_or_all=0
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Выгрузить все",
            cd=cd.send_one_or_all.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=comp_or_post,
                post_id=post_id,
                send_one_or_all=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад",
            cd=cd.select_date.new(
                action=callback_data["action"],
                date=callback_data["date"]
            )
        )
    )
    return keyboard


async def get_post_menu(callback_data: dict, is_in: bool, post_id: int):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 2,
        }
    )
    keyboard.insert(
        await get_inline_button(
            text="Изменить пост",
            cd=cd.change_post.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=0,
                post_id=post_id,
            )
        )
    )
    keyboard.insert(
        await get_inline_button(
            text="Отправить пост",
            cd=cd.send_one_or_all.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=0,
                post_id=post_id,
                send_one_or_all=0
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text=f"{'✅' if not is_in else '❌'}Исключить пост из выгрузки",
            cd=cd.turn_on_or_off_post.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=0,
                post_id=post_id,
                status=not is_in
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Выгрузить все",
            cd=cd.send_one_or_all.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=0,
                post_id=post_id,
                send_one_or_all=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад",
            cd=cd.select_date.new(
                action=callback_data["action"],
                date=callback_data["date"]
            )
        )
    )
    return keyboard


async def select_platform_menu(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    keyboard.add(
        await get_inline_button(
            text="Telegram",
            cd=cd.select_platform.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=callback_data["comp_or_post"],
                post_id=callback_data["post_id"],
                send_one_or_all=callback_data["send_one_or_all"],
                platform="tg"
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад",
            cd=cd.get_post_by_id.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=callback_data["comp_or_post"],
                post_id=callback_data["post_id"]
            )
        )
    )
    return keyboard


async def select_channel(callback_data: dict, user_id: int):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    channels_list = []
    if callback_data["platform"] == "tg":
        channels_list = get_list_telegram_channels(telegram_id=user_id)
    for channel in channels_list:
        keyboard.add(
            await get_inline_button(
                text=channel.name,
                cd=cd.select_channel.new(
                    action=callback_data["action"],
                    date=callback_data["date"],
                    comp_or_post=callback_data["comp_or_post"],
                    post_id=callback_data["post_id"],
                    send_one_or_all=callback_data["send_one_or_all"],
                    platform=callback_data["platform"],
                    channel_id=channel.chat_id
                )
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад",
            cd=cd.send_one_or_all.new(
                action=callback_data["action"],
                date=callback_data["date"],
                comp_or_post=callback_data["comp_or_post"],
                post_id=callback_data["post_id"],
                send_one_or_all=callback_data["send_one_or_all"],
            )
        )
    )
    return keyboard
