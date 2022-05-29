from django.urls import reverse, resolve
from django.test import SimpleTestCase
from ..api.views import (
    CommentListView, CommentCreateView, CommentUpdateDeleteView
)


class CommentUrlTest(SimpleTestCase):
    def test_comment_list_url(self):
        url = reverse('Comment:list_comment', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, CommentListView)

    def test_comment_create_url(self):
        url = reverse('Comment:create_comment', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, CommentCreateView)

    def test_comment_update_delete(self):
        url = reverse('Comment:update_delete_cm', kwargs={'slug': 'slug', 'pk': 1})
        self.assertEquals(resolve(url).func.view_class, CommentUpdateDeleteView)
