from django import forms
from django.conf import settings
from django.urls import NoReverseMatch, reverse


class PreviewMarkdownWidget(forms.Textarea):
    template_name = "markdown_field/widgets/preview.html"

    class Media:
        js = ("markdown_field/markdown_field.js",)

    def __init__(self, field=None, attrs=None):
        super().__init__(attrs)
        self.field = field

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        field_settings = getattr(settings, "MARKDOWN_FIELD", {})
        preview_settings = field_settings.get("preview", {})

        context["widget"]["markdown_field_preview_url"] = self._get_preview_url(
            preview_settings
        )
        context["widget"]["markdown_field_debounce_ms"] = preview_settings.get(
            "debounce_ms", 300
        )
        context["widget"]["markdown_field_cache_key"] = getattr(
            self.field, "_field_cache_key", ""
        )
        return context

    def _get_preview_url(self, preview_settings):
        url = preview_settings.get("url")
        if url:
            return url

        url_name = preview_settings.get("url_name", "markdown_field:preview")
        try:
            return reverse(url_name)
        except NoReverseMatch:
            return ""
