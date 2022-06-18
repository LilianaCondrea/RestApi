from django.contrib import admin
from .models import Blog, Category


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'category',)
    prepopulated_fields = {'slug': ('content',)}
    list_per_page = 20
    search_fields = (
        'content',
        'user__username',
        'category__title'
    )
    filter_horizontal = ('likes',)
    ordering = ('-visited',)
    actions = ['make_published', ]
    list_filter = ('status',)

    @admin.action(description='Publish selected Blogs')
    def make_published(self, request, queryset):
        queryset.update(status='1')
        self.message_user(request, 'Selected Blogs are published')


admin.site.register(Category)
