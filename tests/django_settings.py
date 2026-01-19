USE_TZ = True
SECRET_KEY = "test-secret-key"
ROOT_URLCONF = "tests.urls"

MIDDLEWARE = [
    "django.middleware.csrf.CsrfViewMiddleware",
]

INSTALLED_APPS = [
    "markdown_field",
    "tests",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
    }
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
