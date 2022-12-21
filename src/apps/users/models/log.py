from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    TYPE_CHOICES = (
        (0, 'Создан пост'),
        (1, 'Отредактирован пост'),
        (2, 'Удален пост'),
        (3, 'Создана подборка'),
        (4, 'Удалена подборка'),
        (5, 'Отредактирована подборка'),
        (6, 'Создан гид'),
        (7, 'Удален гид'),
        (8, 'Отредактирован гид')
    )

    datetime = models.DateTimeField('Время')
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True)
    type = models.IntegerField('Тип', choices=TYPE_CHOICES)
    post = models.ForeignKey(to='posts.Post', on_delete=models.SET_NULL, verbose_name='Пост', null=True)
    compilation = models.ForeignKey(to='posts.Compilation', on_delete=models.SET_NULL, verbose_name='Подборка', null=True)
    final_compilation = models.ForeignKey(to='posts.FinalCompilation', on_delete=models.SET_NULL, verbose_name='Гид', null=True)
