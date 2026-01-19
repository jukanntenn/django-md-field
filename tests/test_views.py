import pytest
from django.test import Client
from django.urls import reverse

from markdown_field.cache import register_field
from markdown_field.fields import MarkdownText

pytestmark = pytest.mark.django_db


class TestPreviewView:
    def test_preview_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        url = reverse("markdown_field:preview")
        res = client.post(url, {"text": "## Heading"})
        assert res.status_code == 403

    def test_preview_renders_html(self):
        client = Client(enforce_csrf_checks=True)
        client.get("/csrf/")
        csrf_token = client.cookies["csrftoken"].value

        url = reverse("markdown_field:preview")
        text = "## Heading\n\nThis is a paragraph."
        res = client.post(url, {"text": text, "csrfmiddlewaretoken": csrf_token})
        assert res.status_code == 200
        assert res.json()["html"] == MarkdownText(text).html

    def test_preview_uses_markdown_field_settings(self, settings):
        settings.MARKDOWN_FIELD = {"extensions": ["toc"]}

        client = Client(enforce_csrf_checks=True)
        client.get("/csrf/")
        csrf_token = client.cookies["csrftoken"].value

        url = reverse("markdown_field:preview")
        text = "## Heading\n\nThis is a paragraph."
        res = client.post(url, {"text": text, "csrfmiddlewaretoken": csrf_token})
        assert res.status_code == 200
        assert res.json()["html"] == MarkdownText(text, extensions=["toc"]).html

    def test_preview_uses_field_cache_key(self, settings):
        settings.MARKDOWN_FIELD = {"extensions": ["extra"]}

        field_key = register_field(extensions=["toc"], extension_configs={})

        client = Client(enforce_csrf_checks=True)
        client.get("/csrf/")
        csrf_token = client.cookies["csrftoken"].value

        url = reverse("markdown_field:preview")
        text = "## Heading\n\nThis is a paragraph."
        res = client.post(
            url,
            {
                "text": text,
                "csrfmiddlewaretoken": csrf_token,
                "field_cache_key": field_key,
            },
        )
        assert res.status_code == 200
        # Should use field config (toc), not global settings (extra)
        assert res.json()["html"] == MarkdownText(text, extensions=["toc"]).html
        assert 'id="heading"' in res.json()["html"]
