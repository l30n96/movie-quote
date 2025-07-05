from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Railway-compatible SECRET_KEY handling
SECRET_KEY = os.environ.get("CONFIG_SECRET_KEY") or os.environ.get("SECRET_KEY", "django-insecure-fallback-key-change-in-production")

DEBUG = bool(int(os.environ.get("CONFIG_DEBUG", 0)))

# Fix ALLOWED_HOSTS for Railway
allowed_hosts_env = os.environ.get("CONFIG_ALLOWED_HOSTS", "")
if allowed_hosts_env:
    ALLOWED_HOSTS = allowed_hosts_env.split(", ")
else:
    # Allow Railway domains and common development hosts
    ALLOWED_HOSTS = ['*']  # Railway will handle this, but you can restrict later

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'statistic.apps.StatisticConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added for static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # path to load email templates
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database - Railway PostgreSQL ONLY
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Use Railway's PostgreSQL database
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback to SQLite for local development (no MySQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
PASSWORD_VALIDATOR = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{PASSWORD_VALIDATOR}UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATOR}MinimumLengthValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATOR}CommonPasswordValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATOR}NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
# disabled to solve bugs with statistic visit object creation and complicities
# with different timezones  
USE_TZ = False

# Static files - Railway compatible
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# simplejwt configs
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# swagger configs
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# ipstack api access key
IPSTACK_ACCESS_KEY = os.environ.get("IPSTACK_ACCESS_KEY")

# email configs
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("CONFIG_EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("CONFIG_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("CONFIG_EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_PORT = 587

CORS_ALLOW_ALL_ORIGINS = True

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 259200
    # redirect HTTP request to HTTPS
    SECURE_SSL_REDIRECT = bool(
        int(os.environ.get("CONFIG_SECURE_SSL_REDIRECT", 1)))
    
    # Fix for Railway proxy headers
    proxy_header_env = os.environ.get("CONFIG_SECURE_PROXY_SSL_HEADER")
    if proxy_header_env:
        SECURE_PROXY_SSL_HEADER = tuple(proxy_header_env.split(", "))
    else:
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
