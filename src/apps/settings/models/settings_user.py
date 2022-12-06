from django.db import models
from apps.utils.models import TimeBasedModel


class SettingsUser(TimeBasedModel):
    """Модель всех настроек пользователя"""

    NO_COMMISSION = 0
    WITH_COMMISSION = 1

    FORMULA_CHOICES = (
        (NO_COMMISSION, 'Без комиссии'),
        (WITH_COMMISSION, 'С комиссией')
    )

    user = models.ForeignKey(to='profiles.Profile', verbose_name='Пользователь', on_delete=models.CASCADE)

    currency = models.ForeignKey(to='Currency', verbose_name='Валюта', on_delete=models.CASCADE)
    formula = models.IntegerField('Формула ценообразования', choices=FORMULA_CHOICES, default=NO_COMMISSION)
    commission = models.FloatField('Комиссия', blank=True, null=True, default=0.0)
    rounder = models.IntegerField('Уровень округления', default=1, blank=True, null=True)

    logo = models.ImageField(verbose_name="Логотип", blank=True, null=True)
    text_logo = models.CharField(verbose_name='Текстовый Логотип', max_length=255, blank=True, null=True)
    logo_position = models.CharField(max_length=10, verbose_name='Позиция лого', blank=True, null=True)

    product = models.ForeignKey(to='ProductSettings', verbose_name='Настройки продукт', on_delete=models.CASCADE)

    signature = models.TextField('Подпись', default="")
    link = models.BooleanField('Короткая ссылка', default=False)
    hided_link = models.BooleanField('Ссылка в тексте', default=False)

    def str(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Общую настройку"
        verbose_name_plural = "Общие настройки пользователей"
