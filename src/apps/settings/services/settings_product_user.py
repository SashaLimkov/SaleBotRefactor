from apps.settings.models import ProductSettings, SettingsUser


def add_product_settings(settings_id: int) -> ProductSettings:
    """Создает настройки товара пользователя"""
    return ProductSettings.objects.create(settings_id=settings_id)


def update_field_product_settings(telegram_id: int, field: str, value: bool) -> None:
    """Обновляет поле - field профиля на значение value
    Возможные значения field: link, name, price, discount, sizes, description"""
    profile = SettingsUser.objects.get(profile_id=telegram_id).product_settings
    profile.__setattr__(field, value)
    profile.save()
