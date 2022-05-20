from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from Post.models import Blog


class Comments(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    post = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name=_("Blog")
    )
    comment = models.TextField(
        null=False,
        blank=False,
        verbose_name=_("Comment")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']
