from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(
        max_length=50, null=False, blank=False, verbose_name=_('Title')
    )

    def __str__(self):
        return self.title


class Blog(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_('Author'),

    )
    slug = models.SlugField(
        max_length=100,
        null=True,
        blank=True,
        unique=True
    )
    content = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name=_('Content'),
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name=_('Description'),

    )
    poster = models.ImageField(
        upload_to='post_images',
        null=True,
        blank=True,
        verbose_name=_('Post Image'),
    )
    visited = models.PositiveIntegerField(
        default=0,
        blank=True,
        verbose_name=_('Visited'),
    )
    likes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='likes',
        verbose_name=_('Likes'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        verbose_name=_('Category'),
    )

    allow_comment = models.BooleanField(
        default=True,
        blank=True,
        verbose_name=_('Allow Comment'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created '),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated '),
    )

    def __str__(self):
        return f"{self.user.username} - {self.content}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ['-created_at']
