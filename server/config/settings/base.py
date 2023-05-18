"""
Django settings for safers-dashboard-api project.
"""

from datetime import timedelta
import environ

from functools import partial
from pathlib import Path

from django.utils.text import slugify

import dj_database_url

from safers.core.utils import DynamicSetting
from safers.core.utils import backup_filename_template

#########
# Setup #
#########

env = environ.Env()

ROOT_DIR = Path(__file__).resolve(strict=True).parents[2]  # (server dir)
CONFIG_DIR = ROOT_DIR / "config"
APP_DIR = ROOT_DIR / "safers"

PROJECT_NAME = "Safers Dashboard API"
PROJECT_SLUG = slugify(PROJECT_NAME)
PROJECT_EMAIL = "{role}@" + env("DJANGO_EMAIL_DOMAIN", default="astrosat.net")

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

ROOT_URLCONF = "config.urls"

SITE_ID = 1

APPEND_SLASH = True

DEBUG = False  # redefined in environment module
SECRET_KEY = "shhh"  # redefined in environment module
SECRET_KEY_FALLBACKS = []

########
# Apps #
########

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.gis",
]

THIRD_PARTY_APPS = [
    "colorfield",
    "corsheaders",
    "dbbackup",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "rest_framework_gis",
    "sequences",
    "storages",
]

LOCAL_APPS = [
    "safers.core",
    "safers.users",
    "safers.auth",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

#############
# Databases #
#############

# DATABASE format is: "ENGINE://USER:PASSWORD@HOST:PORT/NAME"

DATABASES = {"default": dj_database_url.config(conn_max_age=0)}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

##############
# Migrations #
##############

MIGRATION_MODULES = {
    # (overrides for app migrations go here)
}

############
# Fixtures #
############

FIXTURE_DIRS = [
    # dirs to search in addtion to fixtures directroy of each app
    # (note that data migrations are preferred to fixtures)
]

########################
# Static & Media Files #
########################

# static & media settings are configured in environment module

###########
# Locales #
###########

# TODO: REVIEW https://docs.djangoproject.com/en/4.1/topics/i18n/timezones/#time-zones

USE_TZ = False
TIME_ZONE = "UTC"
USE_I18N = True
LANGUAGE_CODE = "en-gb"

###########
# Caching #
###########

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",  # name of db table
    },
}

#########
# Admin #
#########

ADMIN_URL = "admin/"

ADMIN_SITE_HEADER = f"{PROJECT_NAME} administration console"
ADMIN_SITE_TITLE = f"{PROJECT_NAME} administration console"
ADMIN_INDEX_TITLE = f"Welcome to the {PROJECT_NAME} administration console"

ADMINS = [(PROJECT_NAME, PROJECT_EMAIL.format(role="techdev"))]
MANAGERS = ADMINS

#############
# Templates #
#############

# any templates placed in "safers/core/templates" can override app-specific templates

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [str(ROOT_DIR / "safers/core/templates"), ],
    # "APP_DIRS": True,  # not needed simce "app_directories.Loader" is specified below
    "OPTIONS": {
        "loaders": [
            "django.template.loaders.filesystem.Loader",  # first look at DIRS
            "django.template.loaders.app_directories.Loader",  # then look in each app
        ],
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.static",
            "django.template.context_processors.tz",
        ],
    },
}]

##############
# Middleware #
##############

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

##################
# Authentication #
##################

# TODO: CREATE A CUSTOM LOGIN TEMPLATE FOR AUTHORIZATION & CLIENT FLOWS ?
LOGIN_URL = "login"

LOGOUT_URL = "logout"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    # TODO: REFACTOR THIS
    "django.contrib.auth.backends.ModelBackend",
]

FUSIONAUTH_API_KEY = env("FUSIONAUTH_API_KEY", default="")
FUSIONAUTH_APPLICATION_ID = env("FUSIONAUTH_APPLICATION_ID", default="")
FUSIONAUTH_CLIENT_ID = env("FUSIONAUTH_CLIENT_ID", default="")
FUSIONAUTH_CLIENT_SECRET = env("FUSIONAUTH_CLIENT_SECRET", default="")
FUSIONAUTH_TENANT_ID = env("FUSIONAUTH_TENANT_ID", default="")
FUSIONAUTH_URL = env("FUSIONAUTH_URL", default="")
FUSIONAUTH_EXTERNAL_URL = env("FUSIONAUTH_EXTERNAL_URL", default=FUSIONAUTH_URL)
FUSIONAUTH_INTERNAL_URL = env("FUSIONAUTH_INTERNAL_URL", default=FUSIONAUTH_URL)
FUSIONAUTH_REDIRECT_URL = env(
    "FUSIONAUTH_REDIRECT_URL", default="http://localhost:8000/auth/callback"
)

#############
# Passwords #
#############

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "safers.users.validators.SafersPasswordValidator"
    },
]

PASSWORD_HASHERS = [
    # the 1st item in this list is the default hasher
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

##################
# Security, etc. #
##################

# TODO: REVIEW THESE...
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

ALLOWED_HOSTS = ["*"]  # redefined in environment module

CLIENT_HOST = env("CLIENT_HOST", default="")

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGIN_REGEXES = [rf"^{CLIENT_HOST}$"]
if DEBUG:
    CORS_ALLOWED_ORIGIN_REGEXES += [r"^https?://localhost(:\d+)?$"]

# (only using cors on the API)
CORS_URLS_REGEX = r"^/api/.*$"

#########
# Email #
#########

# futher email settings (like backend) configured in environment module

EMAIL_TIMEOUT = 60

SERVER_EMAIL = PROJECT_EMAIL.format(
    role='noreply'
)  # email (errors) sent to admins & managers
DEFAULT_FROM_EMAIL = f"{PROJECT_NAME} <{PROJECT_EMAIL.format(role='noreply')}>"  # all other email

#######
# API #
#######

# DRF - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "safers.auth.authentication.OAuth2Authentication",
        # "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
        # "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

FILTERS_DEFAULT_LOOKUP_EXPR = "iexact"

# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": f"{PROJECT_NAME} API",
    "DESCRIPTION": f"Documentation of API endpoints of {PROJECT_NAME}",
    # "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    # "SERVE_AUTHENTICATION": [
    #     "rest_framework.authentication.BasicAuthentication"
    # ],
    "SWAGGER_UI_DIST": "SIDECAR",  # (sidecar allows for local UI configuration)
    "REDOC_DIST": "SIDECAR",
}

###########
# Logging #
###########

# set in environment module

#############
# Profiling #
#############

# set in environment module

###########
# Backups #
###########

DBBACKUP_FILENAME_TEMPLATE = partial(backup_filename_template, PROJECT_SLUG)
DBBACKUP_MEDIA_FILENAME_TEMPLATE = partial(
    backup_filename_template, PROJECT_SLUG
)

# further backups settings are configured in environment module

######################
# App-Specific Stuff #
######################

SAFERS_ALLOW_SIGNUP = DynamicSetting(
    "core.SafersSettings.allow_signup",
    True,
)

SAFERS_ALLOW_SIGNIN = DynamicSetting(
    "core.SafersSettings.allow_signin",
    True,
)

SAFERS_REQUIRE_TERMS_ACCEPTANCE = DynamicSetting(
    "core.SafersSettings.require_terms_acceptance",
    True,
)

SAFERS_GATEWAY_URL = env(
    "SAFERS_GATEWAY_URL",
    default="https://api-test.safers-project.cloud/",
)

SAFERS_GEOSERVER_URL = env(
    "SAFERS_GEOSERVER_URL",
    default="https://geoserver-test.safers-project.cloud/",
)

SAFERS_GEODATA_URL = env(
    "SAFERS_IMPORTER_API_URL",
    default="https://geoapi-test.safers-project.cloud/",
)

SAFERS_DATALAKE_URL = env(
    "SAFERS_DATALAKE_API_URL",
    default="https://datalake-test.safers-project.cloud",
)
