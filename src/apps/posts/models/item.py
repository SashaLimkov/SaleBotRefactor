from django.db import models
from apps.utils.models import TimeBasedModel


class Item(TimeBasedModel):
    """Модель товаров прикрепляемых к посту"""
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост', related_name='items')
    name = models.CharField('Название', max_length=255, null=True, blank=True)
    link = models.CharField('Ссылка', max_length=255, null=True, blank=True)
    sizes = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField('Описание', blank=True, null=True)
    price_old = models.FloatField('Старая цена', default=0)
    price_new = models.FloatField('Новая цена', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар в посте'
        verbose_name_plural = 'Товары в посте'
