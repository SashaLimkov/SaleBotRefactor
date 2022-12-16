from random import randint
from typing import Any

from django.core.files import File

from apps.settings.models import SettingsUser


def add_settings(telegram_id: int) -> SettingsUser:
    """Создает общие настройки пользователя"""
    return SettingsUser.objects.create(profile_id=telegram_id)


def get_settings(telegram_id: int) -> SettingsUser:
    """Возвращает настройки пользователя"""
    return (
        SettingsUser.objects.select_related("product_settings")
        .filter(profile_id=telegram_id)
        .first()
    )


def update_field_settings(telegram_id: int, field: str, value: Any) -> None:
    """Обновляет поле - field профиля на значение value
    Возможные значения field: currency, formula, commission, rounder, logo, text_logo, logo_position,
    signature, link, hided_link"""
    profile = SettingsUser.objects.filter(profile_id=telegram_id).first()
    if profile:
        if field == "logo":
            profile.logo.save(
                str(randint(10000, 9999999)) + "." + value.split(".")[-1],
                File(value),
            )
        else:
            profile.__setattr__(field, value)
        profile.save()
    else:
        raise "Settings not found"
