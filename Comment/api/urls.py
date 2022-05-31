from django.urls import path
from .views import (
    CommentListView, CommentCreateView,
    CommentUpdateDeleteView
)

app_name = 'Comment'

urlpatterns = [
    path('<int:pk>/list_comment/', CommentListView.as_view(), name='list_comment'),
    path('<int:pk>/create_comment/', CommentCreateView.as_view(), name='create_comment'),
    path('<str:slug>/comment/update_delete/<int:pk>/', CommentUpdateDeleteView.as_view(), name='update_delete_cm'),
]
