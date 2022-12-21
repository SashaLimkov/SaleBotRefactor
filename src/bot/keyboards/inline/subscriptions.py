from apps.profiles.services.rate import get_list_rates, get_helper_rate_by_price
from apps.profiles.services.subscription import get_user_active_subscription
from bot.utils.keyboard_utils.base_keyboard_utils import (
    get_base_keyboard,
    get_inline_button,
)
from bot.data import callback_data as cd

__all__ = [
    "get_subscriptions_list_to_buy",
    "get_pay_or_cancel_menu",
    "cancel_invoice",
    "get_helper_subscription_to_buy",
    "get_pay_or_cancel_menu_helper",
    "back_to_main_menu",
]


async def get_subscriptions_list_to_buy(callback_data: dict, is_helper: bool = False):
    rates = get_list_rates()
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    for rate in rates:
        if rate.displayed:
            if not is_helper and rate.price > 1000:
                keyboard.add(
                    await get_inline_button(
                        text=rate.name,
                        cd=cd.rates_menu.new(
                            first_lvl=callback_data["first_lvl"],
                            second_lvl=callback_data["second_lvl"],
                            third_lvl=rate.pk
                        )
                    )
                )
            elif is_helper:
                if rate.price not in (5600, 2000):
                    keyboard.add(
                        await get_inline_button(
                            text=rate.name,
                            cd=cd.rates_menu.new(
                                first_lvl=callback_data["first_lvl"],
                                second_lvl=callback_data["second_lvl"],
                                third_lvl=rate.pk
                            )
                        )
                    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.mm.new(action=callback_data["first_lvl"])
        )
    )
    return keyboard


async def get_pay_or_cancel_menu_helper(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    keyboard.add(
        await get_inline_button(
            text="Оплатить",
            cd=cd.pay_menu_helper.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                rate_pk=callback_data["rate_pk"],
                inviter_id=callback_data["inviter_id"]
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.sub_menu.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"]
            )
        )
    )
    return keyboard


async def get_pay_or_cancel_menu(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    keyboard.add(
        await get_inline_button(
            text="Оплатить",
            cd=cd.pay_menu.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                rate_pk=callback_data["third_lvl"],
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.sub_menu.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"]
            )
        )
    )
    return keyboard


async def cancel_invoice(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.rates_menu.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                third_lvl=callback_data["rate_pk"]
            )
        )
    )
    return keyboard


async def get_helper_subscription_to_buy(callback_data: dict, telegram_id: int):
    inviter_rate_price = get_user_active_subscription(telegram_id=telegram_id).rate.price
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    rate_for_helper = get_helper_rate_by_price(price=inviter_rate_price / 10)
    keyboard.add(
        await get_inline_button(
            text=rate_for_helper.name,
            cd=cd.rate_for_helper_menu.new(
                first_lvl=callback_data["first_lvl"],
                second_lvl=callback_data["second_lvl"],
                rate_pk=rate_for_helper.pk,
                inviter_id=telegram_id
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.mm.new(action=callback_data["first_lvl"])
        )
    )
    return keyboard


async def back_to_main_menu(callback_data: dict = {}):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        }
    )
    keyboard.add(
        await get_inline_button(
            text="◀ В главное меню", cd=cd.MAIN_MENU
        )
    )
    return keyboard
