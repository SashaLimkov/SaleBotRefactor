from apps.profiles.models import Rate

from django.contrib import admin


class RateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rate, RateAdmin)
