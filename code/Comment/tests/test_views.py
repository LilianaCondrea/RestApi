from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from Comment.models import Comments, Reply_Comment
from Post.models import Blog, Category
from Comment.api.serializers import (
    CommentListSerializer, ReplyCommentSerializer,
    CommentCreateUpdateDeleteSerializer
)


class CommentViewApiTest(APITestCase):
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
        self.comment = Comments.objects.create(
            user=self.user1,
            post=self.blog,
            comment='Perfect Blog !',
        )
        self.reply = Reply_Comment.objects.create(
            user=self.user2,
            comment=self.comment,
            reply_text="i agree its great"
        )

    def test_comment_list_status_code(self):
        response = self.client.get(
            reverse('Comment:list_comment', kwargs={'pk': self.blog.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_list_content(self):
        response = self.client.get(
            reverse('Comment:list_comment', kwargs={'pk': self.blog.pk})
        )
        serializer = CommentListSerializer(
            instance=Comments.objects.filter(post=self.blog),
            many=True
        )
        self.assertEqual(response.data, serializer.data)

    def test_comment_list_not_found(self):
        response = self.client.get(
            reverse('Comment:list_comment', kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_create(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token)
        )
        path = reverse('Comment:create_comment', kwargs={'pk': self.blog.pk})
        serializer = CommentCreateUpdateDeleteSerializer(
            data={'comment': 'Awsome Blog !'}
        )
        serializer.is_valid(raise_exception=True)
        response = self.client.post(path, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], 'Awsome Blog !')

    def test_comment_create_more_than_one(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token)
        )
        path = reverse('Comment:create_comment', kwargs={'pk': self.blog.pk})
        serializer = CommentCreateUpdateDeleteSerializer(
            data={'comment': 'Awsome Blog !'}
        )
        serializer.is_valid(raise_exception=True)
        for _ in range(2):
            response = self.client.post(
                path=path,
                data=serializer.data
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_create_authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=None
        )
        path = reverse('Comment:create_comment', kwargs={'pk': self.blog.pk})
        serializer = CommentCreateUpdateDeleteSerializer(
            data={'comment': 'Awsome Blog !'}
        )
        serializer.is_valid(raise_exception=True)
        response = self.client.post(path, serializer.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_update_status_code(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token)
        )
        path = reverse(
            'Comment:update_comment',
            kwargs={'slug': self.blog.slug, 'pk': self.comment.pk}
        )
        serializer = CommentCreateUpdateDeleteSerializer(
            data={'comment': 'Perfect Blog Edited!'}
        )
        serializer.is_valid(raise_exception=True)
        response = self.client.put(path, data=serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_update_content(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token)
        )
        path = reverse(
            'Comment:update_comment',
            kwargs={'slug': self.blog.slug, 'pk': self.comment.pk}
        )
        serializer = CommentCreateUpdateDeleteSerializer(
            data={'comment': 'Perfect Blog Edited!'}
        )
        serializer.is_valid(raise_exception=True)
        response = self.client.put(path, data=serializer.data)
        self.assertEqual(response.data, serializer.data)
        self.assertContains(response, 'Edited')

    def test_comment_update_invalid_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token)
        )
        path = reverse(
            'Comment:update_comment',
            kwargs={'slug': self.blog.slug, 'pk': self.comment.pk}
        )
        response = self.client.put(path, {"comment": "", })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update_authenticate(self):
        path = reverse(
            'Comment:update_comment',
            kwargs={'slug': self.blog.slug, 'pk': self.comment.pk}
        )
        serializer = CommentCreateUpdateDeleteSerializer(
            data={'comment': 'Perfect Blog Edited!'}
        )
        serializer.is_valid(raise_exception=True)
        response = self.client.put(path, data=serializer.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_delete_status_code(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token)
        )
        path = reverse(
            'Comment:delete_comment',
            kwargs={'slug': self.blog.slug, 'pk': self.comment.pk}
        )
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_delete_forbidden(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token)
        )
        path = reverse(
            'Comment:delete_comment',
            kwargs={'slug': self.blog.slug, 'pk': self.comment.pk}
        )
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reply_status_code(self):
        path = reverse(
            'Comment:replies',
            kwargs={'pk': self.comment.pk}
        )
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reply_content(self):
        path = reverse(
            'Comment:replies',
            kwargs={'pk': self.comment.pk}
        )
        serializer = ReplyCommentSerializer(
            Reply_Comment.objects.filter(comment=self.comment),
            many=True
        )
        response = self.client.get(path)
        self.assertEqual(response.data, serializer.data)

    def test_reply_create(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token)
        )
        path = reverse(
            'Comment:reply_create',
            kwargs={'pk': self.comment.pk}
        )
        data = {"reply_text": "Great Blog anyway"}
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reply_create_more_than_one(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token)
        )
        path = reverse(
            'Comment:reply_create',
            kwargs={'pk': self.comment.pk}
        )
        data = {"reply_text": "Great Blog anyway"}
        for _ in range(2):
            response = self.client.post(
                path=path,
                data=data
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reply_create_un_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        path = reverse(
            'Comment:reply_create',
            kwargs={'pk': self.comment.pk}
        )
        data = {"reply_text": "Great Blog anyway"}
        response = self.client.post(
            path=path,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reply_update_status_code(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token)
        )
        path = reverse(
            'Comment:reply_update',
            kwargs={'pk': self.reply.pk}
        )
        data = {"reply_text": "i agree its great edited"}
        response = self.client.put(
            path=path,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reply_update_content(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token)
        )
        path = reverse(
            'Comment:reply_update',
            kwargs={'pk': self.reply.pk}
        )
        data = {"reply_text": "i agree its great edited"}
        response = self.client.put(
            path=path,
            data=data
        )
        self.assertEqual(response.data['reply_text'], data.get('reply_text'))

    def test_reply_update_un_authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=None
        )
        path = reverse(
            'Comment:reply_update',
            kwargs={'pk': self.reply.pk}
        )
        data = {"reply_text": "i agree its great edited"}
        response = self.client.put(
            path=path,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reply_delete_status_code(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user2.access_token)
        )
        path = reverse(
            'Comment:reply_delete',
            kwargs={'pk': self.reply.pk}
        )
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reply_delete_forbidden(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.jwt_user1.access_token)
        )
        path = reverse(
            'Comment:reply_delete',
            kwargs={'pk': self.reply.pk}
        )
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
