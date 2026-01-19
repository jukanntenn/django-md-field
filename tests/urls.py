from django.urls import include, path

from . import views

urlpatterns = [
    path("csrf/", views.csrf, name="csrf"),
    path("markdown-field/", include("markdown_field.urls")),
]
