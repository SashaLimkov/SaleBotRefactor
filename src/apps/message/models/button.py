from django.db import models
from apps.utils.models import TimeBasedModel


class Button(TimeBasedModel):
    """Модель кнопок прикрепляемых к клавиатуре"""
    keyboard = models.ForeignKey('Keyboard', on_delete=models.CASCADE)
    text = models.CharField('Текст', max_length=100, null=True, blank=True)
    url = models.CharField('URL', max_length=255, null=True, blank=True)
    callback_data = models.CharField('Callback Data', max_length=200, null=True, blank=True)
