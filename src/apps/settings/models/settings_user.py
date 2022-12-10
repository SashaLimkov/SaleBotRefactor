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

    SHOP_CURRENCY = 0
    RUB = 1

    CURRENCY_CHOICES = (
        (SHOP_CURRENCY, 'Валюта магазина'),
        (RUB, 'Рубли')
    )

    profile = models.OneToOneField(to='profiles.Profile', to_field='telegram_id',
                                   verbose_name='Пользователь', on_delete=models.CASCADE)

    currency = models.IntegerField('Валюта', choices=CURRENCY_CHOICES, default=SHOP_CURRENCY)
    formula = models.IntegerField('Формула ценообразования', choices=FORMULA_CHOICES, default=NO_COMMISSION)
    commission = models.FloatField('Комиссия', blank=True, null=True, default=0.0)
    rounder = models.IntegerField('Уровень округления', default=0, blank=True, null=True)

    logo = models.ImageField(verbose_name="Логотип", blank=True, null=True)
    text_logo = models.CharField(verbose_name='Текстовый Логотип', max_length=255, blank=True, null=True)
    logo_position = models.CharField(max_length=10, verbose_name='Позиция лого', blank=True, null=True)

    signature = models.TextField('Подпись', default="", blank=True)
    link = models.BooleanField('Короткая ссылка', default=False)
    hided_link = models.BooleanField('Ссылка в тексте', default=False)

    def str(self):
        return f"{self.profile.username}"

    class Meta:
        verbose_name = "Общую настройку"
        verbose_name_plural = "Общие настройки пользователей"
