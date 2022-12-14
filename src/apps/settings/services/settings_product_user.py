from apps.settings.models import ProductSettings, SettingsUser


def add_product_settings(settings_id: int) -> ProductSettings:
    """Создает настройки товара пользователя"""
    return ProductSettings.objects.create(settings_id=settings_id)


def get_product_settings(telegram_id: int) -> ProductSettings:
    return SettingsUser.objects.filter(profile_id=telegram_id).first().product_settings


def update_field_product_settings(telegram_id: int, field: str, value: bool) -> None:
    """Обновляет поле - field профиля на значение value
    Возможные значения field: link, name, price, discount, sizes, description"""
    profile = (
        SettingsUser.objects.filter(profile_id=telegram_id).first().product_settings
    )
    if profile:
        profile.__setattr__(field, value)
        profile.save()
    else:
        raise "Settings not found"
