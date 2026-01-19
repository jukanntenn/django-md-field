## django-md-field Example Project

This is a minimal Django project to demonstrate `django-md-field` in Django Admin.

### Run locally

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Then open:

- http://127.0.0.1:8000/admin/

### Notes

- The `Post.body` field uses `MarkdownField`, so in Django Admin you should see the “编辑 / 预览” tabs.
- The preview endpoint is mounted at `/markdown-field/preview/` and is CSRF-protected.
