import pytest
from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget

from markdown_field.forms import MarkdownFormField
from markdown_field.widgets import PreviewMarkdownWidget

from .models import Post

pytestmark = pytest.mark.django_db


class TestPreviewMarkdownWidget:
    def test_widget_renders_structure(self):
        class PostForm(forms.Form):
            body = MarkdownFormField()

        html = PostForm().as_p()
        assert 'data-md-field="1"' in html
        assert "Write" in html
        assert "Preview" in html
        assert "data-md-preview-url" in html

    def test_widget_renders_with_field_cache_key(self):
        field = Post._meta.get_field("body")
        widget = PreviewMarkdownWidget(field=field)
        context = widget.get_context("body", "", {})

        assert context["widget"]["markdown_field_cache_key"] == field._field_cache_key

    def test_widget_without_field_renders(self):
        widget = PreviewMarkdownWidget()
        context = widget.get_context("body", "", {})

        assert context["widget"]["markdown_field_cache_key"] == ""

    def test_modelform_uses_widget(self):
        class PostModelForm(forms.ModelForm):
            class Meta:
                model = Post
                fields = ["body"]

        form = PostModelForm()
        assert isinstance(form.fields["body"].widget, PreviewMarkdownWidget)

    def test_admin_textarea_override_is_ignored(self):
        model_field = Post._meta.get_field("body")
        form_field = model_field.formfield(widget=AdminTextareaWidget())
        assert isinstance(form_field.widget, AdminTextareaWidget)
