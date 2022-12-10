from django.db import models
from apps.utils.models import TimeBasedModel


class ProductSettings(TimeBasedModel):
    """Модель настроек отображения конретных полей в товаре"""
    settings = models.OneToOneField(to='SettingsUser', primary_key=True,
                                    verbose_name='Настройки', related_name='product_settings', on_delete=models.CASCADE)
    link = models.BooleanField("Ссылка", default=True)
    name = models.BooleanField("Название", default=True)
    price = models.BooleanField("Цена", default=True)
    discount = models.BooleanField("Скидка", default=True)
    sizes = models.BooleanField("Размеры", default=True)
    description = models.BooleanField("Описание", default=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Настройку товара"
        verbose_name_plural = "Настройки товара"
