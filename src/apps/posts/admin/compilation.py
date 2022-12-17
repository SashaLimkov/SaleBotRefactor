from django.contrib import admin
from apps.posts.models import Compilation, FinalCompilation, Content


class ContentInline(admin.StackedInline):
    model = Content
    extra = 0

class FinalCompilationInline(admin.StackedInline):
    model = FinalCompilation
    extra = 0


class CompilationAdmin(admin.ModelAdmin):
    inlines = [FinalCompilationInline, ContentInline]


admin.site.register(Compilation, CompilationAdmin)
admin.site.register(Content)
