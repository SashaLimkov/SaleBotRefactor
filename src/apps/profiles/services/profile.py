from typing import Any

from apps.profiles.models import Profile
from apps.profiles.services.subscription import create_user_subscription
from apps.settings.services.settings_product_user import add_product_settings
from apps.settings.services.settings_user import add_settings
from apps.utils.services.date_time import get_datetime_now


def create_user(telegram_id: int, phone: str, full_name: str, username: str = None, first_name: str = None,
                last_name: str = None, is_helper: bool = False) -> Profile:
    """Создает профиль пользователя и соответствующие настройки"""
    profile = _create_profile(telegram_id, phone, full_name, username, first_name, last_name, is_helper)
    settings = add_settings(telegram_id)
    add_product_settings(settings.id)
    create_user_subscription(telegram_id, 'Старт пробной подписки', 'Пробный')
    return profile


def _create_profile(telegram_id: int, phone: str, full_name: str, username: str = None, first_name: str = None,
                    last_name: str = None, is_helper: bool = False) -> Profile:
    """Создание профиля пользователя бота """
    return Profile.objects.create(telegram_id=telegram_id,
                                  phone=phone,
                                  full_name=full_name,
                                  username=username,
                                  first_name=first_name,
                                  last_name=last_name,
                                  is_helper=is_helper)


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
        raise 'Profile not found'


def update_field_profile(telegram_id: int, field: str, value: Any) -> None:
    """Обновляет поле - field профиля на значение value
    Возможные значения field: is_active, is_helper, is_blocked, in_chat"""
    profile = Profile.objects.filter(telegram_id=telegram_id).first()
    if profile:
        profile.__setattr__(field, value)
        profile.save()
    else:
        raise 'Profile not found'
