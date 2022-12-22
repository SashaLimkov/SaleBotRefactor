import datetime
from typing import Optional, List, Union

from django.db.models import QuerySet
from django.utils import timezone

from apps.profiles.models import Subscription, Rate, Profile
from apps.utils.services.date_time import get_datetime_now
from django.db.models import F


def get_user_active_subscription(telegram_id: int) -> Optional[Subscription]:
    """Получить активную подписку пользователя"""
    profile = Profile.objects.get(telegram_id=telegram_id)
    if profile.is_helper:
        return Subscription.objects.filter(
            profile=profile.inviting_user, active=True
        ).first()
    else:
        return Subscription.objects.filter(profile_id=telegram_id, active=True).first()


def get_all_user_subscriptions(telegram_id: int) -> Optional[List[Subscription]]:
    profile = Profile.objects.get(telegram_id=telegram_id)
    if profile.is_helper:
        return Subscription.objects.filter(
            profile=profile.inviting_user,
        ).all()
    else:
        return Subscription.objects.filter(profile_id=telegram_id).all()


def create_user_subscription(telegram_id: int, cheque: str, rate: str, helper_days: int = None) -> Subscription:
    """Создает новую подписку пользователя"""
    rate = Rate.objects.get(name=rate)
    return Subscription.objects.create(
        profile_id=telegram_id,
        datetime_end=timezone.now() + datetime.timedelta(days=helper_days if helper_days else rate.count_day_sub),
        cheque=cheque,
        rate=rate,
        days_left=helper_days if helper_days else rate.count_day_sub,
    )


def get_user_history_subscriptions(telegram_id: int) -> Union[QuerySet, List[Rate]]:
    """Получение списка всех подписок пользователей"""
    return Subscription.objects.filter(profile_id=telegram_id).select_related(
        "profile", "rate"
    )


def decrement_number_of_days_left() -> None:
    """Декрементация количества дней подписки"""
    Subscription.objects.filter(active=True).only("days_left").update(
        days_left=F("days_left") - 1
    )
    Subscription.objects.filter(days_left=0).only("active").update(active=False)
