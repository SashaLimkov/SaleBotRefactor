from django.db import models

from apps.utils.models import TimeBasedModel
from apps.utils.services.date_time import get_datetime_now


class Profile(TimeBasedModel):
    """Профиль пользователя бота"""
    telegram_id = models.BigIntegerField('ID Telegram', unique=True)
    username = models.CharField('Username Telegram', max_length=255, null=True, blank=True)
    first_name = models.CharField('Имя в Telegram', max_length=255, null=True, blank=True)
    last_name = models.CharField('Фамилия в Telegram', max_length=255, null=True, blank=True)
    registration_date = models.DateTimeField('Дата регистрации', default=get_datetime_now())
    last_action_date = models.DateTimeField('Дата последней активности', default=get_datetime_now())
    activity = models.FloatField('Активность', default=0.0)
    count_actions_in_current_day = models.IntegerField('Количество действий за текущий день', default=0)

    def __str__(self):
        return f'{self.telegram_id}# {self.username} | {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
