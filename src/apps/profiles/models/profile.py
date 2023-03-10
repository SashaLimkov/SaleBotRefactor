from django.db import models
from django.utils import timezone

from apps.utils.models import TimeBasedModel
from apps.utils.services.date_time import get_datetime_now


class Profile(TimeBasedModel):
    """Профиль пользователя бота"""

    is_active = models.BooleanField("Активный", default=True)
    is_helper = models.BooleanField("Помощник", default=False)
    is_blocked = models.BooleanField("Забанен", default=False)
    in_chat = models.BooleanField("В чате", default=False)

    inviting_user = models.ForeignKey(to='self', to_field='telegram_id', verbose_name='Пригласивший пользователь',
                                      on_delete=models.CASCADE, null=True, blank=True)

    telegram_id = models.BigIntegerField('ID Telegram', unique=True, db_index=True)
    username = models.CharField('Username Telegram', max_length=255,  blank=True, default='')
    first_name = models.CharField('Имя в Telegram', max_length=255, blank=True, default='')
    last_name = models.CharField('Фамилия в Telegram', max_length=255, blank=True, default='')

    phone = models.CharField("Номер телефона", max_length=15)
    full_name = models.CharField("ФИО", max_length=255)

    registration_date = models.DateTimeField(
        "Дата регистрации", default=timezone.now
    )
    last_action_date = models.DateTimeField(
        "Дата последней активности", default=timezone.now
    )

    activity = models.FloatField("Активность", default=0.0)

    count_actions_in_current_day = models.IntegerField(
        "Количество действий за текущий день", default=0
    )
    count_days_in_bot = models.IntegerField("Количество дней в боте", default=0)
    count_actions = models.IntegerField("Общее количество действий", default=0)

    def __str__(self):
        return (
            f"{self.telegram_id}# {self.username} | {self.first_name} {self.last_name}"
        )

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
