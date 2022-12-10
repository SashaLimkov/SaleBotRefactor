from django.contrib import admin
from apps.posts.models import Compilation, FinalCompilation


class FinalCompilationInline(admin.StackedInline):
    model = FinalCompilation
    extra = 0


class CompilationAdmin(admin.ModelAdmin):
    inlines = [FinalCompilationInline]


admin.site.register(Compilation, CompilationAdmin)
