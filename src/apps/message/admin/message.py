from apps.message.models import Message, Keyboard, Button

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from django.contrib import admin


class ButtonInline(NestedStackedInline):
    model = Button


class KeyboardAdmin(NestedStackedInline):
    model = Keyboard
    inlines = [ButtonInline]


class MessageAdmin(NestedModelAdmin):
    model = Message
    inlines = [KeyboardAdmin]


admin.site.register(Message, MessageAdmin)
