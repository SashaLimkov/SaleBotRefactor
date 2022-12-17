from django.db import models
from apps.utils.models import TimeBasedModel


class Compilation(TimeBasedModel):
    """Модель подборки"""

    date = models.DateField("Дата")
    name = models.CharField("Подборка", max_length=255)
    done = models.BooleanField("Завершенный обзор", default=False)
    text = models.TextField("Текст поста обзора")

    message_id = models.BigIntegerField("ID Сообщения", blank=True, null=True)

    datetime_send = models.DateTimeField("Время отправки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"


class FinalCompilation(TimeBasedModel):
    """Модель финальной подборки"""

    compilation = models.ForeignKey(
        to="Compilation", on_delete=models.CASCADE, verbose_name="Подборка"
    )
    text = models.TextField("Текст ГИДа")

    message_id = models.BigIntegerField("ID Сообщения", blank=True, null=True)

    def __str__(self):
        return f"{self.compilation.name} | FINAL"

    class Meta:
        verbose_name = "Окончание подборки"
        verbose_name_plural = "Окончания подборок"
