import datetime
from typing import Optional, List, Union

from django.db.models import QuerySet

from apps.profiles.models import Subscription, Rate, Profile
from apps.utils.services.date_time import get_datetime_now
from django.db.models import F


def get_user_active_subscription(telegram_id: int) -> Optional[Subscription]:
    """Получить активную подписку пользователя"""
    profile = Profile.objects.get(telegram_id=telegram_id)
    if profile.is_helper:
        return Subscription.objects.filter(profile=profile.inviting_user, active=True).first()
    else:
        return Subscription.objects.filter(profile=telegram_id, active=True).first()


def create_user_subscription(telegram_id: int, cheque: str, rate: str) -> Subscription:
    """Создает новую подписку пользователя"""
    rate = Rate.objects.get(name=rate)
    return Subscription.objects.create(
        profile_id=telegram_id,
        datetime_end=get_datetime_now() + datetime.timedelta(days=rate.count_day_sub),
        cheque=cheque,
        rate=rate,
        days_left=rate.count_day_sub
    )


def get_user_history_subscriptions(telegram_id: int) -> Union[QuerySet, List[Rate]]:
    """Получение списка всех подписок пользователей"""
    return Subscription.objects.filter(profile_id=telegram_id).select_related('profile', 'rate')


def decrement_number_of_days_left() -> None:
    """Декрементация количества дней подписки"""
    Subscription.objects.filter(active=True).only('days_left').update(days_left=F('days_left') - 1)
    Subscription.objects.filter(days_left=0).only('active').update(active=False)
