from django import forms

from .widgets import PreviewMarkdownWidget


class MarkdownFormField(forms.CharField):
    def __init__(self, field=None, *args, **kwargs):
        kwargs.setdefault("widget", PreviewMarkdownWidget(field=field))
        super().__init__(*args, **kwargs)
