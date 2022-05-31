from django.urls import resolve, reverse
from django.test import SimpleTestCase
from Post.api.views import (
    CategoryListView, BlogListView,
    BlogCreateView, BlogDetailUpdateDeleteView
)


class BlogUrlTest(SimpleTestCase):
    def test_blog_list_url(self):
        url = reverse('Post:blog_list')
        self.assertEqual(resolve(url).func.view_class, BlogListView)

    def test_blog_create_url(self):
        url = reverse('Post:create_blog')
        self.assertEqual(resolve(url).func.view_class, BlogCreateView)

    def test_blog_detail_update_delete_url(self):
        url = reverse('Post:blog_detail', kwargs={'slug': 'slug'})
        self.assertEqual(resolve(url).func.view_class, BlogDetailUpdateDeleteView)

    def test_category_list_url(self):
        url = reverse('Post:category_list')
        self.assertEqual(resolve(url).func.view_class, CategoryListView)
