from django.db import models
from apps.utils.models import TimeBasedModel


class Content(TimeBasedModel):
    """Модель контента прикрепляемого к постам, подборкам, финальным подборкам"""

    PHOTO = 0
    VIDEO = 1
    AUDIO = 2
    DOCUMENT = 3

    TYPE_CHOICES = (
        (PHOTO, "Фотография"),
        (VIDEO, "Видео"),
        (AUDIO, "Аудио"),
        (DOCUMENT, "Документ"),
    )

    post = models.ForeignKey(
        to="Post",
        on_delete=models.CASCADE,
        related_name="contents",
        verbose_name="Пост",
    )
    file = models.FileField("Файл", upload_to="post_content")
    type = models.IntegerField("Тип файла", choices=TYPE_CHOICES)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
