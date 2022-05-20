from django.test import TestCase
from django.contrib.auth import get_user_model
from Post.models import Blog


class BlogTestApiView(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_superuser(
            username='testuser1',
            email='testemail1@gmail.com',
            password='testpassword1',
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='testemail2',
            password='testpassword2',
        )
        # Create a blog
        self.blog = Blog.objects.create(
            content='test content',
            description='test description',
            user=self.user1,
        )

    def test_blog_list(self):
        response = self.client.get('/api/blog/blogs/')
        self.assertEqual(response.status_code, 200)

