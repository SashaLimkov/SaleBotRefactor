from apps.profiles.models import Profile, Subscription

from django.contrib import admin


class SubscriptionInline(admin.TabularInline):
    model = Subscription


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    inlines = [SubscriptionInline]


admin.site.register(Profile, ProfileAdmin)
