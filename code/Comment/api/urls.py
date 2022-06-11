from django.urls import path
from .views import (
    CommentListView, CommentCreateView,
    CommentUpdateDeleteView,ReplyCommentListCreateView,
    ReplyCommentUpdateDeleteView
)

app_name = 'Comment'

urlpatterns = [
    path('<int:pk>/list_comment/', CommentListView.as_view(), name='list_comment'),
    path('<int:pk>/create_comment/', CommentCreateView.as_view(), name='create_comment'),
    path('<str:slug>/comment/update/<int:pk>/', CommentUpdateDeleteView.as_view(), name='update_comment'),
    path('<str:slug>/comment/delete/<int:pk>/', CommentUpdateDeleteView.as_view(), name='delete_comment'),
    
    path('create_reply/<int:pk>/', ReplyCommentListCreateView.as_view(), name='reply_create'),
    path('replies/<int:pk>/', ReplyCommentListCreateView.as_view(), name='replies'),
    path('update_reply/<int:pk>/', ReplyCommentUpdateDeleteView.as_view(), name='reply_update'),
    path('delete_reply/<int:pk>/', ReplyCommentUpdateDeleteView.as_view(), name='reply_delete'),



]
    