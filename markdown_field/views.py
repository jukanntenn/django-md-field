from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .cache import get_field_config
from .fields import MarkdownText


@method_decorator(csrf_protect, name="dispatch")
@method_decorator(require_http_methods(["POST"]), name="dispatch")
class PreviewMarkdownView(View):
    def post(self, request, *args, **kwargs):
        field_cache_key = request.POST.get("field_cache_key", "")

        field_config = {}
        if field_cache_key:
            field_config = get_field_config(field_cache_key) or {}

        markdown_field_settings = getattr(settings, "MARKDOWN_FIELD", {})

        extensions = field_config.get(
            "extensions", markdown_field_settings.get("extensions", [])
        )
        extension_configs = field_config.get(
            "extension_configs", markdown_field_settings.get("extension_configs", {})
        )

        text = request.POST.get("text", "")
        html = MarkdownText(
            text,
            extensions=extensions,
            extension_configs=extension_configs,
        ).html
        return JsonResponse({"html": html})
