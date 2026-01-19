import warnings
from html.parser import HTMLParser

import markdown
from django.conf import settings
from django.db.models.fields import TextField
from django.db.models.query_utils import DeferredAttribute

from .cache import register_field
from .forms import MarkdownFormField
from .widgets import PreviewMarkdownWidget


class TOCHTMLParser(HTMLParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ul_cnt = 0
        self._ul_start_line = None
        self._ul_start_pos = None
        self._ul_end_line = None
        self._ul_end_pos = None
        self.html = ""

    def error(self, message):
        warnings.warn(message)

    def handle_starttag(self, tag, attrs):
        if tag == "ul":
            if self._ul_cnt == 0:
                self._ul_start_line, self._ul_start_pos = self.getpos()
            self._ul_cnt += 1

    def handle_endtag(self, tag):
        if tag == "ul":
            self._ul_cnt -= 1
            if self._ul_cnt == 0:
                self._ul_end_line, self._ul_end_pos = self.getpos()
                lines = self.rawdata.split("\n")
                lines = lines[self._ul_start_line - 1 : self._ul_end_line]
                lines[-1] = lines[-1][: self._ul_end_pos]
                lines[0] = lines[0][self._ul_start_pos + 4 :]
                self.html = "".join(lines)


class MarkdownText:
    def __init__(self, text, **kwargs):
        self._md = markdown.Markdown(**kwargs)
        self._text = text
        self._html = None
        self._toc = None

    @property
    def text(self):
        return self._text

    @property
    def html(self):
        return self._convert()

    @property
    def toc(self):
        self._convert()
        return self._toc

    def _convert(self):
        if self._html is None:
            self._html = self._md.convert(self._text)
            if hasattr(self._md, "toc"):
                # If there is no content, set `toc` to an empty string instead of wrapping it in a `div` tag.
                parser = TOCHTMLParser()
                parser.feed(self._md.toc)
                self._toc = parser.html

        return self._html

    def __str__(self):
        return self._text


class MarkdownDescriptor(DeferredAttribute):
    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        text = super().__get__(instance, cls)
        if isinstance(text, str):
            instance.__dict__[self.field.attname] = self.field.attr_class(
                text, **self.field.get_markdown_kwargs()
            )

        return instance.__dict__[self.field.attname]

    def __set__(self, instance, value):
        instance.__dict__[self.field.attname] = value


class MarkdownField(TextField):
    attr_class = MarkdownText
    descriptor_class = MarkdownDescriptor

    def __init__(self, *args, **kwargs):
        self._extensions = kwargs.pop("extensions", None)
        self._extension_configs = kwargs.pop("extension_configs", None)
        super().__init__(*args, **kwargs)

        markdown_kwargs = self.get_markdown_kwargs()
        self._field_cache_key = register_field(
            markdown_kwargs["extensions"],
            markdown_kwargs["extension_configs"],
        )

    def to_python(self, value):
        if isinstance(value, MarkdownText) or value is None:
            return value

        text = super().to_python(value)
        return MarkdownText(text, **self.get_markdown_kwargs())

    def get_prep_value(self, value):
        if isinstance(value, MarkdownText):
            return str(value)

        return value

    def get_markdown_kwargs(self):
        markdown_field_settings = getattr(settings, "MARKDOWN_FIELD", {})
        return {
            "extensions": self._extensions
            or markdown_field_settings.get("extensions", []),
            "extension_configs": self._extension_configs
            or markdown_field_settings.get("extension_configs", {}),
        }

    def formfield(self, **kwargs):
        kwargs.setdefault("form_class", MarkdownFormField)
        kwargs.setdefault("widget", PreviewMarkdownWidget(field=self))
        return super().formfield(**kwargs)
