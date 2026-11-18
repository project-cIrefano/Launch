from pathlib import Path
import os
from urllib.parse import parse_qs, unquote, urlparse
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
# Load optional local secrets without requiring a third-party dotenv package.
# Existing OS values take priority; load .env.local before .env so it wins.
for local_env in (BASE_DIR / ".env.local", BASE_DIR / ".env"):
    if local_env.is_file():
        for line in local_env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                os.environ.setdefault(name.strip(), value.strip().strip("\"'"))
IS_VERCEL = os.environ.get("VERCEL") == "1"
DEBUG_DEFAULT = "False" if IS_VERCEL else "True"
DEBUG = os.environ.get("DJANGO_DEBUG", DEBUG_DEFAULT).lower() in {"1", "true", "yes"}
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Set DJANGO_SECRET_KEY when DJANGO_DEBUG is disabled.")
    SECRET_KEY = "dev-only-change-this-key-before-deployment"
elif not DEBUG and SECRET_KEY.startswith(("dev-only-", "replace-this-")):
    raise ImproperlyConfigured("Replace the example DJANGO_SECRET_KEY before disabling Django debug mode.")
configured_hosts = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]
if IS_VERCEL:
    vercel_hosts = [
        os.environ[name].strip()
        for name in ("VERCEL_URL", "VERCEL_BRANCH_URL", "VERCEL_PROJECT_PRODUCTION_URL")
        if os.environ.get(name, "").strip()
    ]
    ALLOWED_HOSTS = list(dict.fromkeys(configured_hosts + vercel_hosts))
    if not ALLOWED_HOSTS:
        ALLOWED_HOSTS = [".vercel.app"]
    CSRF_TRUSTED_ORIGINS = [
        "https://*.vercel.app",
        *[
            f"https://{host}"
            for host in dict.fromkeys(configured_hosts + vercel_hosts)
            if not host.startswith(".") and "*" not in host
        ],
    ]
else:
    local_hosts = [
        host.strip()
        for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
        if host.strip()
    ]
    ALLOWED_HOSTS = local_hosts
    CSRF_TRUSTED_ORIGINS = [
        origin.strip()
        for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
        if origin.strip()
    ]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "store.apps.StoreConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "store.context_processors.cart_summary",
        ],
    },
}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
DB_ENGINE = os.environ.get("DB_ENGINE", "sqlite").lower()
if DATABASE_URL:
    database_url = urlparse(DATABASE_URL)
    if database_url.scheme not in {"postgres", "postgresql"}:
        raise ImproperlyConfigured("DATABASE_URL must use the postgres:// or postgresql:// scheme.")
    if not database_url.path.strip("/"):
        raise ImproperlyConfigured("DATABASE_URL must include a database name.")

    database_options = {}
    url_options = parse_qs(database_url.query)
    sslmode = url_options.get("sslmode", ["require" if IS_VERCEL else ""])[0]
    if sslmode:
        database_options["sslmode"] = sslmode

    DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(database_url.path.lstrip("/")),
        "USER": unquote(database_url.username or ""),
        "PASSWORD": unquote(database_url.password or ""),
        "HOST": database_url.hostname or "",
        "PORT": str(database_url.port or 5432),
        "OPTIONS": database_options,
        "CONN_MAX_AGE": 0,
    }}
elif DB_ENGINE == "mysql":
    import pymysql
    pymysql.install_as_MySQLdb()
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "taza_food_corner"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }}
elif IS_VERCEL:
    raise ImproperlyConfigured(
        "Vercel needs a persistent database. Set DATABASE_URL for PostgreSQL, "
        "or set DB_ENGINE=mysql with the DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, and DB_PORT variables."
    )
else:
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

# Browser permissions are requested only after a visitor clicks the location button.
# Geolocation works on localhost during development and on HTTPS in production.
SECURE_CONTENT_TYPE_NOSNIFF = True
# OpenStreetMap's public tile servers require web pages to send a valid Referer.
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
