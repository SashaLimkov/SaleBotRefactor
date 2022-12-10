from django.db import models
from apps.utils.models import TimeBasedModel


class ChanelTelegram(TimeBasedModel):
    """Модель Telegram каналов прикрепляемых к пользователю"""
    profile = models.ForeignKey(to='profiles.Profile', to_field='telegram_id',
                                on_delete=models.CASCADE, verbose_name='Пользователь')
    chat_id = models.BigIntegerField('ID Канала')
    name = models.CharField('Название канала', max_length=255)

    def __str__(self):
        return f'TG: {self.profile.telegram_id} | {self.chat_id}'

    class Meta:
        verbose_name = 'Канал в Telegram'
        verbose_name_plural = 'Каналы в Telegram'


class ChanelVk(TimeBasedModel):
    """Модель ВК каналов прикрепляемых к пользователю"""
    profile = models.ForeignKey(to='profiles.Profile', to_field='telegram_id',
                                on_delete=models.CASCADE, verbose_name='Пользователь')
    chat_id = models.BigIntegerField('ID Канала')

    def __str__(self):
        return f'VK: {self.profile.telegram_id} | {self.chat_id}'

    class Meta:
        verbose_name = 'Канал в ВК'
        verbose_name_plural = 'Каналы в ВК'
