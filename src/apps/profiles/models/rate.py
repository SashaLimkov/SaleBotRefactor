from django.db import models
from apps.utils.models import TimeBasedModel


class Rate(TimeBasedModel):
    """Модель тарифов для подписок"""
    displayed = models.BooleanField('Отображается', default=True)
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    price = models.FloatField('Цена')
    currency = models.CharField('Идентификатор валюты', max_length=5)
    count_day_sub = models.IntegerField('Количество дней подписки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
