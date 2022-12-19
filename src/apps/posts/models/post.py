from django.db import models
from apps.utils.models import TimeBasedModel


class Post(TimeBasedModel):
    """Модель постов отправляемых пользователю"""

    compilation = models.ForeignKey(
        to="Compilation", verbose_name="Подборка", on_delete=models.CASCADE, null=True
    )
    shop = models.ForeignKey(
        to="Shop", verbose_name="Магазин", on_delete=models.CASCADE
    )
    message_id = models.BigIntegerField("ID Сообщения", blank=True, null=True)

    def __str__(self):
        return f"{self.shop}|{self.compilation}"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class UserPost(TimeBasedModel):
    """Модель пользовательских постов"""

    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name="user_post", verbose_name="Пост"
    )
    profile = models.ForeignKey(
        to="profiles.Profile",
        to_field="telegram_id",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    text = models.TextField("Текст поста")

    def __str__(self):
        return f"{self.post.shop}|{self.post.compilation}|{self.profile.username}"

    class Meta:
        verbose_name = "Пост пользователя"
        verbose_name_plural = "Посты пользователей"
