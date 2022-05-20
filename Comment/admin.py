from django.contrib import admin
from Comment.models import Comments


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment',)

