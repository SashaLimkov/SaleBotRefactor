from django.db import models
from apps.utils.models import TimeBasedModel


class Post(TimeBasedModel):
    """Модель постов отправляемых пользователю"""
    compilation = models.ForeignKey(to='Compilation', verbose_name="Подборка", on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(to='Shop', verbose_name="Магазин", on_delete=models.CASCADE)
    message_id = models.BigIntegerField('ID Сообщения', blank=True, null=True)

    datetime_send = models.DateTimeField('Время отправки')

    def __str__(self):
        return f"{self.shop}|{self.compilation}"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
