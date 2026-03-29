# personal_site/settings.py

from pathlib import Path
from decouple import config, Csv
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core Settings ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-^k8#p!x9z2w@q5v$m*f7c4b1n%j6t3h+r_y(d-g=s&l0')
DEBUG = config('DEBUG', default=False, cast=bool)

# Updated to include your custom domains
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='sudheeshsathya.com,www.sudheeshsathya.com,web-production-668f18.up.railway.app', cast=Csv())

# --- Application Definition ---
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Restored for static files
    'django.contrib.staticfiles',
    'background_task',
    'home.apps.HomeConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Restored: Must be below SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'personal_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'personal_site.wsgi.application'

# --- Database ---
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600
    )
}

# --- Site Configuration ---
SITE_DOMAIN = config('SITE_DOMAIN', default='https://sudheeshsathya.com')
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='https://sudheeshsathya.com,https://www.sudheeshsathya.com', cast=Csv())

# --- Jazzmin UI Configuration ---
JAZZMIN_SETTINGS = {
    "site_title": "Sudheesh Sathya",
    "site_header": "MyBlog",
    "welcome_sign": "Welcome to the MyBlog Admin Panel",
    "copyright": "Sudheesh Sathya Ltd.",
    "search_model": "home.Post",
    "show_sidebar": True,
    "navigation_expanded": True,
}

# --- Static and Media Files ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Using WhiteNoise for efficient static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure media directory exists for Railway Volume
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# --- Email Configuration ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='sudheeshsathya12@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='dfkqxvuomguwcnjr')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --- Production Security Settings ---
# CRITICAL: This line fixes the "Too Many Redirects" error on Railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'