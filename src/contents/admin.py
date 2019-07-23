# from django.contrib import admin

# from .models import Category, Content

# class CategoryManager(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name', 'description')
#     list_filter = ('name',)
#     prepopulated_fields = {'slug': ('name',)}

# admin.site.register(Category, CategoryManager)

# class ContentManager(admin.ModelAdmin):
#     list_display = ('title', 'category', 'author', 'status', 'created', 'modified', 'published')
#     search_fields = ('title', 'content', 'category')
#     list_filter = ('category', 'status', 'author', 'created', 'modified')
#     prepopulated_fields = {'slug': ('title',)}


# admin.site.register(Content, ContentManager)

from django.contrib import admin

from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    # list_display = ('name', )
    # search_fields = ('name', )
    # list_filter = ('name', )
    prepopulated_fields = {'slug': ('title', )}