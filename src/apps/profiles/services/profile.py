from datetime import datetime
from typing import Any, Union, List, Optional

from apps.profiles.services.subscription import create_user_subscription
from apps.settings.services.settings_product_user import add_product_settings
from apps.settings.services.settings_user import add_settings
from apps.utils.services.date_time import get_datetime_now
from apps.profiles.models import Profile, Subscription

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import CharField, Prefetch, QuerySet


def create_user(
    telegram_id: int,
    phone: str,
    full_name: str,
    username: str = '',
    first_name: str = '',
    last_name: str = '',
    is_helper: bool = False,
) -> Profile:
    """Создает профиль пользователя и соответствующие настройки"""
    profile = _create_profile(
        telegram_id, phone, full_name, username, first_name, last_name, is_helper
    )
    settings = add_settings(telegram_id)
    add_product_settings(settings.id)
    create_user_subscription(telegram_id, "Старт пробной подписки", "Пробный")
    return profile


def _create_profile(telegram_id: int, phone: str, full_name: str, username: str = '', first_name: str = '',
                    last_name: str = '', is_helper: bool = False) -> Profile:
    """Создание профиля пользователя бота"""
    return Profile.objects.create(
        telegram_id=telegram_id,
        phone=phone,
        full_name=full_name,
        username=username,
        first_name=first_name,
        last_name=last_name,
        is_helper=is_helper,
    )


def get_profile_by_telegram_id(telegram_id: int) -> Profile:
    """Возвращает Profile пользователя по telegram_id"""
    return Profile.objects.filter(telegram_id=telegram_id).first()


def get_profile_is_helper(telegram_id: int) -> bool:
    """Проверяет, является ли пользователь помощником"""
    return Profile.objects.filter(telegram_id=telegram_id).first().is_helper


def update_last_action_date_profile(telegram_id: int) -> None:
    """Обновляет время последнего действия пользователя и инкрементирует количество действий"""
    profile = Profile.objects.filter(telegram_id=telegram_id).first()
    if profile:
        profile.last_action_date = get_datetime_now()
        profile.count_actions_in_current_day += 1
        profile.save()
    else:
        raise "Profile not found"


def update_field_profile(telegram_id: int, field: str, value: Any) -> None:
    """Обновляет поле - field профиля на значение value
    Возможные значения field: is_active, is_helper, is_blocked, in_chat"""
    profile = Profile.objects.filter(telegram_id=telegram_id).first()
    if profile:
        profile.__setattr__(field, value)
        profile.save()
    else:
        raise "Profile not found"


def get_search_profiles_queryset(search: str,
                                 date_start: Optional[datetime.date],
                                 date_end: Optional[datetime.date]) -> Union[QuerySet, List[Profile]]:
    """Получить QuerySet пользователей с поиском по строке search"""
    vector = TrigramSimilarity('phone', search) + TrigramSimilarity('username', search) \
                  + TrigramSimilarity('full_name', search) + TrigramSimilarity(
        Cast('telegram_id', output_field=CharField()), search)
    prefetch_subscription = Prefetch('subscription_set', queryset=Subscription.objects.filter(active=True))
    queryset = Profile.objects.prefetch_related(prefetch_subscription).annotate(similarity=vector).filter(
            similarity__gt=0.35).order_by('-similarity')
    return queryset


def get_all_profiles_queryset(date_start: Optional[datetime.date],
                              date_end: Optional[datetime.date]) -> Union[QuerySet, List[Profile]]:
    """Получить QuerySet пользователей"""
    return Profile.objects.all().prefetch_related(Prefetch('subscription_set',
                                                           queryset=Subscription.objects.filter(active=True)))


def get_subscribe_profile_queryset(queryset: QuerySet) -> Union[QuerySet, List[Profile]]:
    """Привязать поле с информацией об активной подписке к существующему QuerySet"""
    for item in queryset:
        item.subscription_active = item.subscription_set.all()
    return queryset
