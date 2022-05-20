from django.urls import path
from .views import (
    CommentListView, CommentCreateView, CommentDetailDeleteView, CommentUpdateView
)

app_name = 'Comment'

urlpatterns = [
    path('list_comment/', CommentListView.as_view(), name='list_comment'),
    path('<int:pk>/create_comment/', CommentCreateView.as_view(), name='create_comment'),
    path('comment/<int:pk>/', CommentDetailDeleteView.as_view(), name='cm_detail_delete'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),
]
