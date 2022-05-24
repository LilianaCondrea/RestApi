from django.contrib import admin
from .models import Blog, Category


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'category',)
    prepopulated_fields = {'slug': ('content',)}


admin.site.register(Category)
