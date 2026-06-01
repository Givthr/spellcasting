from pathlib import Path
import os
import dj_database_url 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-&0jch_y3^c_z3jm7nv%(p#3q@37$e93)!b#t(_3c3cmrvb8w)a")

DEBUG = os.environ.get("DEBUG", "True") == "True"

# --- FIX: Dynamically parse ALLOWED_HOSTS from env strings ---
if not DEBUG:
    ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
else:
    ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bee",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spelling_bee_pro.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "spelling_bee_pro.wsgi.application"

# Database Configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- FIX: Secure & modern dynamic database extraction ---
if os.environ.get('DATABASE_URL'):
    ssl_require = os.environ.get("DATABASE_SSL_REQUIRE", "True") == "True"
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600, 
        ssl_require=ssl_require
    )

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- STATIC CONFIGURATION FOR PRODUCTION ---
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / 'static'] 
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- AUTHENTICATION FLOW ROUTING ---
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# --- CSRF and Security Settings for Production Environments ---
# Adding explicit fallback arrays solves the 403 error loops across production builds.
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'https://spellcasting-production.up.railway.app',
        'http://127.0.0.1:8000',
        'http://localhost:8000'
    ]
    
    # Optional fallback parser if you pass variables dynamically down the road
    env_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
    if env_origins:
        CSRF_TRUSTED_ORIGINS += env_origins.split(",")
        
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_REFERRER_POLICY = "same-origin"

# --- WHITENOISE VIDEO STREAM FIXES FOR RAILWAY ---
WHITENOISE_MIME_TYPES = {
    '.mp4': 'video/mp4'
}

WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mp3', 'wav')
