from django import forms

from markdown_field.forms import MarkdownFormField
from markdown_field.widgets import PreviewMarkdownWidget


class TestMarkdownFormField:
    def test_form_field_uses_preview_widget(self):
        field = MarkdownFormField()
        assert isinstance(field.widget, PreviewMarkdownWidget)

    def test_form_field_without_field_param(self):
        field = MarkdownFormField()
        assert field.widget.field is None

    def test_form_field_with_field_param(self):
        from .models import Post

        post_field = Post._meta.get_field("body")
        form_field = MarkdownFormField(field=post_field)
        assert form_field.widget.field == post_field

    def test_form_field_can_be_used_in_form(self):
        class PostForm(forms.Form):
            body = MarkdownFormField()

        form = PostForm()
        assert "body" in form.fields
        assert isinstance(form.fields["body"], MarkdownFormField)

    def test_form_field_accepts_widget_override(self):
        class CustomWidget(forms.Textarea):
            pass

        field = MarkdownFormField(widget=CustomWidget())
        assert isinstance(field.widget, CustomWidget)
