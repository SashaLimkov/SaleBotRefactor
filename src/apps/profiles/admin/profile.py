import asyncio

from django.shortcuts import render

from apps.profiles.forms import MessageForm
from apps.profiles.models import Profile, Subscription, ProfileMetric
from apps.settings.models import (
    ChanelTelegram,
    ChanelVk,
    SettingsUser,
    ProductSettings,
    CourseUser,
)

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from django.contrib import admin, messages

from bot.utils.message_worker import spam_machine


class UsersFilter(admin.SimpleListFilter):
    title = "Фильтр По Пользователям"
    parameter_name = ""
    field_name = ""

    def lookups(self, request, model_admin):
        return ((1, "Только подписчики"), (2, "Все исключая подписчиков"), (3, "Все, у кого есть дни доступа"))

    def queryset(self, request, queryset):
        res = self.value()
        if not res:
            return queryset
        res = int(res)
        if res == 1:
            return queryset.filter(in_chat=True)
        if res == 2:
            return queryset.filter(in_chat=False)
        if res == 3:
            return queryset.filter(subscription__days_left__gt=0, subscription__active=True)


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
    list_filter = (UsersFilter,)
    actions = [
        "send_messages",
    ]
    loop = asyncio.new_event_loop()

    def send_messages(self, request, queryset):
        if "message" in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data["message"]
                chats = queryset.all()
                for chat in chats:
                    print(chat.telegram_id)
                messages.success(request, "Рассылка сообщений началась")
                self.loop.run_until_complete(spam_machine(message, chats))
                messages.success(request, "Рассылка сообщений завершилась")
                return
        else:
            form = MessageForm()
        return render(
            request,
            "action_send_message.html",
            {
                "title": "Напишите сообщение",
                "chats": queryset,
                "form": form,
            },
        )

    send_messages.short_description = "Рассылка сообщения"


admin.site.register(Profile, ProfileAdmin)
