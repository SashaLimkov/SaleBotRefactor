from django.contrib import admin
from apps.settings.models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Currency, CurrencyAdmin)
