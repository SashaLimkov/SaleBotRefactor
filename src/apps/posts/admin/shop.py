from django.contrib import admin
from apps.posts.models import Shop


class ShopAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)
