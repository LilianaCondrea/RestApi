from django.urls import path
from .views import BlogListView, BlogDetailUpdateDeleteView, BlogCreateView, CategoryListView

app_name = "Post"

urlpatterns = [
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blog/<str:slug>/', BlogDetailUpdateDeleteView.as_view(), name='blog_detail'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
]
