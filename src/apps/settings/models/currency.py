from django.db import models
from apps.utils.models import TimeBasedModel


class Currency(TimeBasedModel):
    """Модель валют"""
    name = models.CharField('Название валюты (в боте)', max_length=20)
    currency = models.CharField('Валюта', max_length=4)
    sign = models.CharField('Знак валюты', max_length=1, blank=True, null=True)

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
