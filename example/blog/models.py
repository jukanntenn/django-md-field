from django.conf import settings
from django.db import models
from django.utils import timezone

from markdown_field import MarkdownField


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = MarkdownField("body", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    enable_comments = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="user",
        related_name="posts",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
