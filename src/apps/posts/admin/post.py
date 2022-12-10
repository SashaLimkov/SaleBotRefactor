from django.contrib import admin
from apps.posts.models import Content, Item, Post, UserPost


class ContentInline(admin.StackedInline):
    model = Content
    extra = 0


class ItemInline(admin.StackedInline):
    model = Item
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [ContentInline, ItemInline]


class UserPostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(UserPost, UserPostAdmin)

