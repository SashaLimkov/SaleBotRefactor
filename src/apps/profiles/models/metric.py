from django.db import models
from apps.utils.models import TimeBasedModel


class ProfileMetric(TimeBasedModel):
    """Метрики пользователя бота"""

    profile = models.ForeignKey(
        to="Profile", to_field="telegram_id", on_delete=models.CASCADE
    )
    date = models.DateField()
    count_actions = models.IntegerField()
