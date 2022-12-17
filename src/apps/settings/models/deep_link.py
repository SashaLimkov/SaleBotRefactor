from django.db import models
from apps.utils.models import TimeBasedModel


class DeepLink(TimeBasedModel):
    """Модель одноразовых диплинков для помощников"""
    creator_id = models.BigIntegerField("ИД создателя диплинки")
    deep_link = models.CharField("Диплинк", max_length=255)
    identifier = models.BigIntegerField("Идентификатор")
    used = models.BooleanField("Использован", default=False)

    class Meta:
        verbose_name = "Диплинк"
        verbose_name_plural = "Диплинки"
