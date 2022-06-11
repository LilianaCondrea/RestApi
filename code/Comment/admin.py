from django.contrib import admin
from Comment.models import Comments, Reply_Comment


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment',)


@admin.register(Reply_Comment)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment',)
