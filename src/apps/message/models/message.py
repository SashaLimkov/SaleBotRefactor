from django.db import models
from apps.utils.models import TimeBasedModel
from django.contrib.postgres.indexes import BrinIndex


class Message(TimeBasedModel):
    """Модель сообщений подгружаемых в бота"""
    name = models.CharField('Название', max_length=60, unique=True)  # Поле используемое для получения сообщений из бота
    text = models.TextField('Текст', null=True, blank=True)

    def __str__(self):
        return f'{self.pk}# {self.name}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MessageContent(TimeBasedModel):
    """Поля содержащие контент сообщений"""
    message = models.ForeignKey(to=Message, on_delete=models.SET_NULL, null=True, verbose_name='Сообщение')
    file = models.FileField('Файл')

