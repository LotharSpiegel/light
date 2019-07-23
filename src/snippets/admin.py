from django.contrib import admin

from .models import Language, Snippet

admin.site.register(Snippet)


class LanguageManager(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'language_code')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Language, LanguageManager)