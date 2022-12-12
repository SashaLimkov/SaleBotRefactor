from django.db import models
from apps.utils.models import TimeBasedModel


class Shop(TimeBasedModel):
    """Модель магазинов"""

    name = models.CharField("Название магазина", max_length=255)
    currency = models.ForeignKey(
        to="settings.Currency", on_delete=models.CASCADE, verbose_name="Валюта магазина"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
