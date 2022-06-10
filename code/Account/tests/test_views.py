from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from Account.api.serializers import UserListSerializer, UserDetailSerializer


class AccountViewApiTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_superuser(
            username='firstuser',
            email='firstuser10@email.com',
            phone=12345678910,
            password='Firstuser!123',
        )
        self.jwt_user1 = RefreshToken.for_user(self.user1)
        # ---------------------------------------
        self.user2 = get_user_model().objects.create_user(
            username='seconduser',
            email='seconduser20@email.com',
            phone=12345678920,
            password='Seconduser!123',
        )
        self.jwt_user2 = RefreshToken.for_user(self.user2)
        # ----------------------------------
        self.user3 = get_user_model().objects.create_user(
            username='thirduser',
            email='thirduser30@email.com',
            phone=12345678930,
            password='thirduser!123',
        )
        self.jwt_user3 = RefreshToken.for_user(self.user3)

    def test_user_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user1.access_token}"
        )
        response = self.client.get(reverse('Account:user_list'))
        data = get_user_model().objects.all()
        factory = APIRequestFactory()
        request = factory.get(reverse('Account:user_list'))
        serializer = UserListSerializer(
            data, many=True, context={'request': request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), len(data))
        self.assertEqual(response.data[0]['username'], data[0].username)

    def test_user_detail_view(self):
        response = self.client.get(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk}))
        data = get_user_model().objects.get(id=self.user2.pk)
        factory = APIRequestFactory()
        request = factory.get(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk}))
        serializer = UserDetailSerializer(data, context={'request': request})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_user_update_view(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user2.access_token}",
        )
        response = self.client.put(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk}),
            {
                'username': 'new_username',
                'email': 'new_username2@email.com',
                'phone': 12345678920,
                'password': 'new_password!123',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['username'], 'seconduser')
        self.assertEqual(response.data['username'], 'new_username')

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user3.access_token}"
        )
        response = self.client.put(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk}),
            {
                'username': 'new_username',
                'email': 'new_username2@email.com',
                'phone': 12345678920,
                'password': 'new_password!123',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 403)

    def test_user_delete_view(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user3.access_token}"
        )
        response = self.client.delete(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk})
        )

        self.assertEqual(response.status_code, 403)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user2.access_token}",
        )
        response = self.client.delete(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk})
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(get_user_model().objects.filter(
            id=self.user2.pk).exists())
        self.assertEqual(get_user_model().objects.count(), 2)
