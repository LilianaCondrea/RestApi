import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import status
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

    def test_user_list_status_code(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user1.access_token}"
        )
        response = self.client.get(reverse('Account:user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_data(self):
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
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data[0]['username'], response.data[0]['username'])

    def test_user_list_len(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user1.access_token}"
        )
        response = self.client.get(reverse('Account:user_list'))
        data = get_user_model().objects.all()
        self.assertEqual(len(response.data), len(data))

    def test_user_list_unauthorized(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=None
        )
        response = self.client.get(reverse('Account:user_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_forbidden(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user2.access_token}"
        )
        response = self.client.get(reverse('Account:user_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_user_search(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user1.access_token}"
        )
        response = self.client.get(reverse('Account:user_list') + f"?search={self.user1.email}")
        self.assertEqual(len(response.data), 1)

    def test_list_user_wrong_search(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user1.access_token}"
        )
        response = self.client.get(reverse('Account:user_list') + f"?search=wrong_keyword")
        self.assertFalse(response.data)

    def test_list_user_filter(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user1.access_token}"
        )
        response = self.client.get(reverse('Account:user_list') + "?is_superuser=false")
        self.assertTrue(response.data)
        self.assertEqual(len(response.data), get_user_model().objects.filter(is_superuser=False).count())

    def test_list_user_wrong_filter(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user1.access_token}"
        )
        response = self.client.get(reverse('Account:user_list') + "?is_superuser=yes")
        self.assertEqual(len(response.data), get_user_model().objects.all().count())

    def test_list_user_ordering(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user1.access_token}"
        )
        response = self.client.get(reverse('Account:user_list') + "?ordering=date_joined")

        self.assertEqual(response.data[0]['username'], f"{self.user1.username}")

    def test_user_detail_status_code(self):
        response = self.client.get(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_found(self):
        response = self.client.get(
            reverse('Account:user_detail', kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_content(self):
        response = self.client.get(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk})
        )
        data = get_user_model().objects.get(id=self.user2.pk)
        factory = APIRequestFactory()
        request = factory.get(
            reverse('Account:user_detail', kwargs={'pk': self.user2.pk}))
        serializer = UserDetailSerializer(data, context={'request': request})
        self.assertEqual(response.data, serializer.data)

    def test_user_update_status_code(self):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_status_code_without_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user3.access_token}",
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_content(self):
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
        self.assertNotEqual(response.data['username'], self.user2.username)

    def test_user_delete_with_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user3.access_token}"
        )
        response = self.client.delete(
            reverse('Account:user_detail', kwargs={'pk': self.user3.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(get_user_model().objects.filter(id=self.user3.id).exists())

    def test_user_delete_without_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user2.access_token}"
        )
        response = self.client.delete(
            reverse('Account:user_detail', kwargs={'pk': self.user3.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_without_authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=None
        )
        response = self.client.delete(
            reverse('Account:user_detail', kwargs={'pk': self.user3.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_status_code(self):
        response = self.client.get(
            reverse("Account:user_profile", kwargs={'pk': self.user2.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_not_found(self):
        response = self.client.get(
            reverse("Account:user_profile", kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_profile_update(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user2.access_token}"
        )
        update_data = {
            "first_name": "updated_first",
            "last_name": "updated_last",
            "gender": "M",
        }
        response = self.client.put(
            reverse("Account:user_profile", kwargs={'pk': self.user2.pk}),
            data=update_data
        )
        info = json.loads(response.content)
        self.assertEqual(info.get("first_name"), update_data.get("first_name"))

    def test_user_profile_wrong_update(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user2.access_token}"
        )

        response = self.client.put(
            reverse("Account:user_profile", kwargs={'pk': self.user2.pk}),
            data={"gender": "Wrong"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile_delete(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user2.access_token}"
        )
        response = self.client.delete(
            reverse("Account:user_profile", kwargs={'pk': self.user2.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_profile_delete_forbidden(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.jwt_user3.access_token}"
        )
        response = self.client.delete(
            reverse("Account:user_profile", kwargs={'pk': self.user2.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
