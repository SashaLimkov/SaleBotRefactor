from datetime import datetime
from typing import Any, Union, List, Optional

from django.utils import timezone

from apps.profiles.services.subscription import create_user_subscription
from apps.settings.services.settings_product_user import add_product_settings
from apps.settings.services.settings_user import add_settings
from apps.utils.services.date_time import get_datetime_now
from apps.profiles.models import Profile, Subscription

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import CharField, Prefetch, QuerySet, Q


def create_user(
        telegram_id: int,
        phone: str,
        full_name: str,
        days_left: int = 0,
        username: str = '',
        first_name: str = '',
        last_name: str = '',
        is_helper: bool = False,
        helper_days: int = None,
        rate: str = None,
        cheque: str = None,
        inviter_id: int = None
) -> Profile:
    """Создает профиль пользователя и соответствующие настройки"""
    profile = _create_profile(
        telegram_id, phone, full_name, username, first_name, last_name, is_helper, inviter_id
    )
    settings = add_settings(telegram_id)
    add_product_settings(settings.id)
    sub = create_user_subscription(telegram_id, "Старт пробной подписки" if not cheque else cheque,
                                   "Пробный" if not rate else rate, helper_days=helper_days)
    if days_left:
        sub.days_left += days_left - 30
        sub.save()
    return profile


def _create_profile(telegram_id: int, phone: str, full_name: str, username: str = '', first_name: str = '',
                    last_name: str = '', is_helper: bool = False, inviter_id: int = None) -> Profile:
    """Создание профиля пользователя бота"""
    return Profile.objects.create(
        telegram_id=telegram_id,
        phone=phone,
        full_name=full_name,
        username=username,
        first_name=first_name,
        last_name=last_name,
        is_helper=is_helper,
    ) if not inviter_id else Profile.objects.create(telegram_id=telegram_id,
                                                    phone=phone,
                                                    full_name=full_name,
                                                    username=username,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    is_helper=is_helper,
                                                    inviting_user_id=inviter_id
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
        profile.last_action_date = timezone.now()
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


def get_search_profiles_queryset(search: str, filter_date: Q) -> Union[QuerySet, List[Profile]]:
    """Получить QuerySet пользователей с поиском по строке search"""
    vector = TrigramSimilarity('phone', search) + TrigramSimilarity('username', search) \
             + TrigramSimilarity('full_name', search) + TrigramSimilarity(
        Cast('telegram_id', output_field=CharField()), search)
    prefetch_subscription = Prefetch('subscription_set', queryset=Subscription.objects.filter(active=True))
    if not filter_date:
        queryset = Profile.objects.prefetch_related(prefetch_subscription).annotate(similarity=vector).filter(
            similarity__gt=0.35).order_by('-similarity')
    else:
        queryset = Profile.objects.prefetch_related(prefetch_subscription).annotate(similarity=vector).filter(
            filter_date, similarity__gt=0.35).order_by('-similarity')
    return queryset


def get_all_profiles_queryset(filter_date: Q) -> Union[QuerySet, List[Profile]]:
    """Получить QuerySet пользователей"""
    prefetch_subscription = Prefetch('subscription_set', queryset=Subscription.objects.filter(active=True))
    if filter_date:
        return Profile.objects.filter(filter_date).prefetch_related(prefetch_subscription)
    else:
        return Profile.objects.all().prefetch_related(prefetch_subscription)


def get_date_range_profiles_filter(date_start: Optional[datetime.date],
                                   date_end: Optional[datetime.date]) -> Q:
    """Получение фильтра по дате регистрации"""
    return Q(registration_date__gte=date_start, registration_date__lte=date_end)


def get_subscribe_profile_queryset(queryset: QuerySet) -> Union[QuerySet, List[Profile]]:
    """Привязать поле с информацией об активной подписке к существующему QuerySet"""
    for item in queryset:
        item.subscription_active = item.subscription_set.all()
    return queryset


def get_inviting_user_profile(telegram_id: int) -> Profile:
    """Получить объект пригласившего пользователя по telegram_id помощника"""
    return Profile.objects.get(telegram_id=telegram_id).inviting_user


def get_list_helpers_profile(telegram_id: int) -> Union[QuerySet, List[Profile]]:
    """Возвращает список всех помощников пользователя"""
    return Profile.objects.get(telegram_id=telegram_id).profile_set.all()
