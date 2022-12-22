from apps.profiles.services.subscription import get_all_user_subscriptions


async def get_user_days(telegram_id: int) -> int:
    subs = get_all_user_subscriptions(telegram_id=telegram_id)
    days = 0
    for sub in subs:
        days += sub.days_left
    return days
