from django.urls import reverse, resolve
from django.test import SimpleTestCase
from Account.api.views import (
    UserListView, UserDetailView, ProfileUserView
)


class AccountUrlTest(SimpleTestCase):
    def test_user_list_url(self):
        url = reverse('Account:user_list')
        self.assertEqual(resolve(url).func.view_class, UserListView)

    def test_user_detail_url(self):
        url = reverse('Account:user_detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, UserDetailView)

    def test_profile_user_url(self):
        url = reverse('Account:user_profile', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ProfileUserView)
