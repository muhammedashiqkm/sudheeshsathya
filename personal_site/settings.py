# personal_site/settings.py

from pathlib import Path
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core Settings ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-^k8#p!x9z2w@q5v$m*f7c4b1n%j6t3h+r_y(d-g=s&l0')
# Set DEBUG=False in your Railway variables!
DEBUG = config('DEBUG', default=False, cast=bool)
# Use the Railway variables to pass your domains (e.g., sudheeshsathya.com, your-app.up.railway.app)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

# --- Application Definition ---
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Essential for local development with WhiteNoise
    'django.contrib.staticfiles',
    'background_task',
    'home.apps.HomeConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essential for Railway static files
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
# Railway automatically provisions the DATABASE_URL environment variable when you link a PostgreSQL database.
# The default fallback here allows you to use a local SQLite database for testing if the variable isn't set.
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3')),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# --- Site & Contact Configuration ---
SITE_DOMAIN = config('SITE_DOMAIN', default='http://127.0.0.1:8000')
CONTACT_EMAIL = config('CONTACT_EMAIL', default='')

# --- Security & CSRF (Crucial for Railway) ---
# Railway puts your app behind a secure proxy. This tells Django to trust HTTPS headers from Railway.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Add your actual domains here in your Railway environment variables so form submissions work
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://127.0.0.1', cast=Csv())

# On Railway, set these to 'True' in your environment variables for production security
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)


# --- Jazzmin UI Configuration ---
JAZZMIN_SETTINGS = {
    "site_title": "Sudheesh Sathya",
    "site_header": "MyBlog",
    "welcome_sign": "Welcome to the MyBlog Admin Panel",
    "copyright": "Sudheesh Sathya Ltd.",
    "search_model": "home.Post",
    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static and Media Files (Configured for Railway & WhiteNoise) ---
STATIC_URL = '/static/'
# This ensures WhiteNoise compresses and creates unique hashes for your static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Note: Railway's disk is ephemeral. Any files uploaded here via the admin panel will be deleted upon redeployment 
# unless you set up an external storage bucket (like AWS S3) or attach a persistent volume in Railway.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- Email Configuration ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='sudheeshsathya12@gmail.com')
# Removed hardcoded password. You MUST set this in Railway Variables!
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='put_your_password_here')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'