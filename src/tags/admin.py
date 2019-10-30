from django.contrib import admin

from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    list_filter = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    pass