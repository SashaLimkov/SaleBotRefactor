from django.db import models
from django.utils import timezone

from apps.utils.models import TimeBasedModel
from apps.utils.services.date_time import get_datetime_now


class Subscription(TimeBasedModel):
    """Модель активной подписки пользователя"""

    active = models.BooleanField("Активна", default=True)
    profile = models.ForeignKey(
        to="Profile",
        to_field="telegram_id",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    datetime_buy = models.DateTimeField("Время покупки", default=timezone.now)
    datetime_end = models.DateTimeField("Время окончания подписки")
    cheque = models.CharField("Чек", max_length=255, null=True, blank=True)
    rate = models.ForeignKey(
        to="Rate", on_delete=models.SET_NULL, null=True, verbose_name="Тариф"
    )
    days_left = models.IntegerField("Осталось дней")

    def __str__(self):
        return f"{self.profile} - {self.rate.name} | {self.days_left}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
