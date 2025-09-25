from pathlib import Path
from datetime import timedelta

# ---------------------
# BASE SETTINGS
# ---------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-wnbi7sbw5m^!a953f&+6t!xixym-3dk)x-5hpsyc^ztwrz&$dc'
DEBUG = True
ALLOWED_HOSTS = []

# ---------------------
# APPLICATIONS
# ---------------------
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'drf_yasg',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',

    # Local apps
    'bridal_api.apps.BridalApiConfig',
]

# ---------------------
# MIDDLEWARE
# ---------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware
    'bridal_api.middleware.bridal_middleware.BannedIPMiddleware',
    'bridal_api.middleware.bridal_middleware.RateLimitMiddleware',
    'bridal_api.middleware.bridal_middleware.RequestLoggingMiddleware',
    'bridal_api.middleware.bridal_middleware.DressViewCountMiddleware',
    'bridal_api.middleware.bridal_middleware.CustomHeaderMiddleware',
]

# ---------------------
# URLS & WSGI
# ---------------------
ROOT_URLCONF = 'project_nexus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project_nexus.wsgi.application'

# ---------------------
# DATABASE
# ---------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bridal_db',
        'USER': 'bridal_user',
        'PASSWORD': 'YourStrongPassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ---------------------
# AUTHENTICATION & REST FRAMEWORK
# ---------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 4,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ---------------------
# LOGGING
# ---------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# ---------------------
# PASSWORD VALIDATION
# ---------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------
# INTERNATIONALIZATION
# ---------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------
# STATIC & MEDIA FILES
# ---------------------
STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------
# CORS CONFIGURATION
# ---------------------
CORS_ALLOW_ALL_ORIGINS = True

# ---------------------
# CUSTOM SETTINGS
# ---------------------
BANNED_IPS = [
    # Example: "203.0.113.1",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User model
AUTH_USER_MODEL = "bridal_api.User"
