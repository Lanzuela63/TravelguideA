from pathlib import Path
import os
import sys
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / 'backend'))

# Core Directories
FRONTEND_DIR = BASE_DIR / "frontend"
BACKEND_DIR = BASE_DIR / "backend"
SHARED_STATIC_DIR = BASE_DIR / "shared" / "static"

# SECURITY
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-dev-secret")  # Default for dev
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in ["true", "1", "yes"]
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")]

# Apps
INSTALLED_APPS = [
    # Local apps
    "apps.tourism",
    "apps.users",
    "apps.content",
    "apps.ar",
    "apps.events",
    "apps.business",
    "apps.dashboards",

    # 3rd-party apps
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Django built-in apps
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

SITE_ID = 1

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "bicoltravelguide.urls"
WSGI_APPLICATION = "bicoltravelguide.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            FRONTEND_DIR / "templates",
            BACKEND_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "travelguide_db",
        "USER": "postgres",
        "PASSWORD": "N3t0p1@boy",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Authentication
AUTH_USER_MODEL = "users.CustomUser"
LOGIN_REDIRECT_URL = "/dashboards/"

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [SHARED_STATIC_DIR]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:19006",  # Expo
    "http://127.0.0.1:8000",   # Django dev
    "http://10.0.2.2:8000",    # Emulator
]
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

# Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
