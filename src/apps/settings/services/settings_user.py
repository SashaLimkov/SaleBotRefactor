from random import randint
from typing import Any

from django.core.files import File

from apps.settings.models import SettingsUser


def add_settings(telegram_id: int) -> SettingsUser:
    """Создает общие настройки пользователя"""
    return SettingsUser.objects.create(profile_id=telegram_id)


def get_settings(telegram_id: int) -> SettingsUser:
    """Возвращает настройки пользователя"""
    return SettingsUser.objects.select_related('product_settings').get(profile_id=telegram_id)


def update_field_settings(telegram_id: int, field: str, value: Any) -> None:
    """Обновляет поле - field профиля на значение value
    Возможные значения field: currency, formula, commission, rounder, logo, text_logo, logo_position,
    signature, link, hided_link"""
    profile = SettingsUser.objects.get(profile_id=telegram_id)
    if field == 'logo':
        with open(value, "rb") as file:
            profile.logo.save(
                str(randint(10000, 9999999)) + "." + value.split(".")[-1], File(file)
            )
    else:
        profile.__setattr__(field, value)
    profile.save()
