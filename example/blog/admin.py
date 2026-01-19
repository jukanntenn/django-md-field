from django.contrib import admin

from markdown_field.widgets import PreviewMarkdownWidget
from markdown_field.fields import MarkdownField

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "enable_comments")
    list_filter = ("enable_comments", "author")
    search_fields = ("title", "body")
    formfield_overrides = {MarkdownField: {"widget": PreviewMarkdownWidget}}

    class Media:
        css = {"all": ("blog/css/markdown-preview.css",)}
