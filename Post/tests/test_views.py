from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from Post.models import Category, Blog
from Post.api.serializers import BlogDetailSerializer, BlogListSerializer, BlogCreateSerializer


class BlogViewApiTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='firstuser',
            email='firstuser@email.com',
            phone=12345678910,
            password='Seconduser!123',
        )
        self.jwt_user1 = RefreshToken.for_user(self.user1)

        self.user2 = get_user_model().objects.create_user(
            username='seconduser',
            email='seconduser20@email.com',
            phone=12345678920,
            password='seconduser!123',
        )
        self.jwt_user2 = RefreshToken.for_user(self.user2)

        self.category = Category.objects.create(
            title='Django Test'
        )

        self.blog = Blog.objects.create(
            content='Test Blog',
            description='testing project with drf framework',
            allow_comment=True,
            user=self.user1,
            category=self.category
        )

        self.blog2 = Blog.objects.create(
            content='Test Blog2',
            description='testing project with drf framework2',
            allow_comment=True,
            user=self.user2,
            category=self.category
        )

    def test_blog_list(self):
        response = self.client.get(
            reverse('Post:blog_list'),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertContains(response, 'Test Blog')

    def test_blog_detail(self):
        serializer = BlogDetailSerializer(instance=Blog.objects.get(id=self.blog.id))
        response = self.client.get(
            reverse('Post:blog_detail', kwargs={'slug': self.blog.slug}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
        self.assertContains(response, 'Test Blog')

    def test_blog_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        serializer = BlogCreateSerializer(data={
            'content': 'New Blog',
            'description': 'New Blog for testing the project',
            'allow_comment': True,
            'category': self.category.id,
            'poster': None
        })
        serializer.is_valid(raise_exception=True)
        response = self.client.post(
            reverse('Post:create_blog'),
            data=serializer.data,
            format='json'
        )

        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token))
        serializer = BlogCreateSerializer(data={
            'content': 'New Blog',
            'description': 'New Blog for testing the project',
            'allow_comment': True,
            'category': self.category.id,
            'poster': None
        })
        serializer.is_valid(raise_exception=True)
        response = self.client.post(
            reverse('Post:create_blog'),
            data=serializer.data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data['allow_comment'])

    def test_blog_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token))
        serializer = BlogDetailSerializer(
            data={
                'content': 'Test Blog3',
                'description': 'testing project with drf framework3',
                'allow_comment': True,
                'category': self.category.id,
                'poster': None
            })
        serializer.is_valid(raise_exception=True)
        response = self.client.put(
            reverse('Post:blog_detail', kwargs={'slug': self.blog.slug}),
            data=serializer.data,
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
        self.assertContains(response, 'Test Blog3')
        self.assertNotEqual(response.data, self.blog.content)

    def test_blog_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        response = self.client.delete(
            reverse('Post:blog_detail', kwargs={'slug': self.blog.slug}),
        )
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token))
        response = self.client.delete(
            reverse('Post:blog_detail', kwargs={'slug': self.blog.slug}),
        )
        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token))
        response = self.client.delete(
            reverse('Post:blog_detail', kwargs={'slug': self.blog.slug}),
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
