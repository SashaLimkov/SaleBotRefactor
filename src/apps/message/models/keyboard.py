from django.db import models
from apps.utils.models import TimeBasedModel


class Keyboard(TimeBasedModel):
    """Модель клавиатуры прикрепляемой к сообщению"""

    REPLY = 0
    INLINE = 1

    TYPE_CHOICES = ((REPLY, "Reply"), (INLINE, "Inline"))

    type = models.IntegerField("Тип", choices=TYPE_CHOICES)
    one_time_keyboard = models.BooleanField("Одноразовая клавиатура", default=False)
    row_width = models.IntegerField("Количество кнопок в ряду")
    message = models.OneToOneField(
        to="Message",
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Сообщение",
    )
