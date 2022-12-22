from django.db import models
from apps.utils.models import TimeBasedModel


class CourseUser(TimeBasedModel):
    """Модель курса валют пользователей"""

    currency = models.ForeignKey(
        to="Currency",
        to_field="currency",
        on_delete=models.CASCADE,
        verbose_name="Валюта",
    )
    profile = models.ForeignKey(
        to="profiles.Profile",
        to_field="telegram_id",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    value = models.FloatField("Значение")

    def __str__(self):
        return f"{self.currency} - {self.value}"

    class Meta:
        verbose_name = "Курс валют пользователя"
        verbose_name_plural = "Курсы валют пользователей"
