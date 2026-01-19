# django-md-field

A Django model field that integrates [Python-Markdown](https://github.com/Python-Markdown/markdown) for handling Markdown content.

## Requirements

- Python: >=3.10, <4
- Django: >=4.2, <6.0

## Installation

```bash
pip install django-md-field
```

## Usage

### Basic Usage

```python
from django.db.models import Model
from markdown_field import MarkdownField

class Post(Model):
    body = MarkdownField("body")
```

### GitHub-style Write/Preview Form Field

This package provides a GitHub-like “Write / Preview” experience for forms by default.

#### Enable templates/static

Add the app:

```python
INSTALLED_APPS = [
    # ...
    "markdown_field",
]
```

Include the preview endpoint:

```python
from django.urls import include, path

urlpatterns = [
    # ...
    path("markdown-field/", include("markdown_field.urls")),
]
```

#### Usage in forms

- In a `ModelForm`, `MarkdownField` will use the preview widget by default.
- In a plain `Form`, use:

```python
from django import forms
from markdown_field.forms import MarkdownFormField

class PostForm(forms.Form):
    body = MarkdownFormField()
```

#### CSRF requirement

The preview request is CSRF-protected. Make sure your form template contains:

```django
{% csrf_token %}
```

The frontend code reads the token from the form input (`csrfmiddlewaretoken`), not from cookies.

#### Styling

This library ships no CSS on purpose. Style it yourself using the following stable hooks:

- `.md-field`
- `.md-field__tabs`, `.md-field__tab`
- `.md-field__pane`
- `.md-field__preview`
- `.markdown-body` (optional hook if you want to use a GitHub-like markdown stylesheet)

#### Preview settings

```python
MARKDOWN_FIELD = {
    "extensions": [...],
    "extension_configs": {...},
    "preview": {
        "url_name": "markdown_field:preview",  # or set "url" to an absolute/relative URL
        "debounce_ms": 300,
    },
}
```

### Accessing Content

```python
# Create a post with Markdown content
>>> post = Post.objects.create(body="## Heading\n\nThis is a paragraph.")

# Access the raw Markdown text
>>> post.body.text
'## Heading\n\nThis is a paragraph.'

# Access the rendered HTML
>>> post.body.html
'<h2>Heading</h2>\n<p>This is a paragraph.</p>'

# Access table of contents (if TOC extension is enabled)
>>> post.body.toc
'<li><a href="#heading">Heading</a></li>'
```

### Configuring Markdown Extensions

You can configure Markdown extensions in two ways:

- In your Django settings (`settings.py`):

```python
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

MARKDOWN_FIELD = {
    "extensions": [
        TocExtension(slugify=slugify, toc_depth=3),
        "pymdownx.highlight",
        "pymdownx.arithmatex",
    ],
    "extension_configs": {
        "pymdownx.highlight": {
            "linenums_style": "pymdownx-inline",
        },
        "pymdownx.arithmatex": {
            "generic": True,
        },
    },
}
```

- Directly in the model field, this will override the `MARKDOWN_FIELD` setting in `settings.py`:

```python
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

body = MarkdownField(
    "body",
    extensions=[
        TocExtension(slugify=slugify, toc_depth=3),
        "pymdownx.highlight",
        "pymdownx.arithmatex",
    ],
    extension_configs={
        "pymdownx.highlight": {
            "linenums_style": "pymdownx-inline",
        },
        "pymdownx.arithmatex": {
            "generic": True,
        },
    },
)
```

For more information about available extensions, see:

- [Python Markdown Extensions](https://python-markdown.github.io/extensions/)
- [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/)

## Security

Preview returns HTML rendered from Markdown. Depending on your extensions and usage, you may need to sanitize the output or restrict allowed extensions to avoid XSS risks.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
