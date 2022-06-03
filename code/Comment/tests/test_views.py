from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from Comment.api.serializers import CommentListSerializer, CommentCreateUpdateDeleteSerializer
from Comment.models import Comments
from Post.models import Blog, Category


class CommentViewApiTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='firstuser',
            email='firstuser@email.com',
            phone=12345678910,
            password='Seconduser!123',
        )
        self.jwt_user1 = RefreshToken.for_user(self.user1)
        # ----------------------------------
        self.user2 = get_user_model().objects.create_user(
            username='seconduser',
            email='seconduser20@email.com',
            phone=12345678920,
            password='seconduser!123',
        )
        self.jwt_user2 = RefreshToken.for_user(self.user2)
        # ----------------------------------
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
        self.comment = Comments.objects.create(
            user=self.user1,
            post=self.blog,
            comment='Perfect Blog !',
        )
        # ----------------------------------

    def test_comment_list(self):
        response = self.client.get(
            reverse('Comment:list_comment', kwargs={'pk': self.blog.pk})
        )
        serializer = CommentListSerializer(instance=Comments.objects.filter(post=self.blog), many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Perfect Blog !')

    def test_comment_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token))
        path = reverse('Comment:create_comment', kwargs={'pk': self.blog.pk})
        serializer = CommentCreateUpdateDeleteSerializer(
            data={'comment': 'Awsome Blog !'}
        )
        serializer.is_valid(raise_exception=True)
        response = self.client.post(path, serializer.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['comment'], 'Awsome Blog !')

    def test_comment_update(self):
        path = reverse(
            'Comment:update_delete_cm', kwargs={'slug': self.blog.slug, 'pk': self.comment.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token))
        serializer = CommentCreateUpdateDeleteSerializer(
            data={'comment': 'Perfect Blog Edited!'}
        )
        serializer.is_valid(raise_exception=True)
        response = self.client.put(path, data=serializer.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
        self.assertNotEqual(self.comment, response.data)
        self.assertContains(response, ' Edited!')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token))
        response = self.client.put(path, data=serializer.data)
        self.assertEqual(response.status_code, 403)

    def test_comment_delete(self):
        path = reverse(
            'Comment:update_delete_cm', kwargs={'slug': self.blog.slug, 'pk': self.comment.pk}
        )

        self.client.credentials(HTTP_AUTHORIZATION=None)
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token))
        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, 204)
