from django.urls import path
from django.views.i18n import JavaScriptCatalog

from . import views

app_name = "markdown_field"

urlpatterns = [
    path(
        "jsi18n/", JavaScriptCatalog.as_view(packages=["markdown_field"]), name="jsi18n"
    ),
    path("preview/", views.PreviewMarkdownView.as_view(), name="preview"),
]
