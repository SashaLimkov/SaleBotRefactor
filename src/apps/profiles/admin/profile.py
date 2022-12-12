from apps.profiles.models import Profile, Subscription, ProfileMetric
from apps.settings.models import (
    ChanelTelegram,
    ChanelVk,
    SettingsUser,
    ProductSettings,
    CourseUser,
)

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from django.contrib import admin


class HelpersProfileInline(NestedStackedInline):
    model = Profile
    verbose_name = "Помощник"
    verbose_name_plural = "Помощники"
    extra = 0


class ChanelTelegramInline(NestedStackedInline):
    model = ChanelTelegram
    extra = 0


class ChanelVkInline(NestedStackedInline):
    model = ChanelVk
    extra = 0


class ProductSettingsInline(NestedStackedInline):
    model = ProductSettings
    extra = 1


class SettingsUserInline(NestedStackedInline):
    model = SettingsUser
    inlines = [ProductSettingsInline]
    extra = 1


class SubscriptionInline(NestedStackedInline):
    model = Subscription
    extra = 0


class CourseUserInline(NestedStackedInline):
    model = CourseUser
    extra = 0


class ProfileMetricInline(NestedStackedInline):
    model = ProfileMetric
    extra = 0


class ProfileAdmin(NestedModelAdmin):
    inlines = [
        SettingsUserInline,
        HelpersProfileInline,
        SubscriptionInline,
        ChanelTelegramInline,
        ChanelVkInline,
        CourseUserInline,
        ProfileMetricInline,
    ]


admin.site.register(Profile, ProfileAdmin)
