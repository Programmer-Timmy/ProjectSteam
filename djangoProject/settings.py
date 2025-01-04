# Django settings for djangoProject project.

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-kw88(jr8w%pje579@7hc4-0&-h$ionl!-66eul3^ed$p*(l76n'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Custom user model
AUTH_USER_MODEL = 'AuthManager.CustomUser'
LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/dashboard'
LOGOUT_REDIRECT_URL = '/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'dashboard.apps.DashboardConfig',
    'steam.apps.SteamConfig',
    'AuthManager',
    'games.apps.GamesConfig',
    'ajax.apps.AjaxConfig',
    'account.apps.AccountConfig',
    'social_django',
    'daily_check',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'djangoProject.wsgi.application'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [BASE_DIR / "djangoProject/static"]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
ASGI_APPLICATION = 'djangoProject.asgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'steam',
        'USER': 'postgres',
        'PASSWORD': 'Postgresdumdums',
        'HOST': '85.144.230.126',
        'PORT': '5432',
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Social Auth settings
SOCIAL_AUTH_USER_MODEL = 'AuthManager.CustomUser'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'AuthManager.pipeline.create_or_update_user',  # Custom pipeline
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',  # Associate by email
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_STEAM_EXTRA_DATA = ['avatar']  # Make sure this is set correctly

# Social authentication backends
AUTHENTICATION_BACKENDS = [
    'social_core.backends.steam.SteamOpenId',  # Correct Steam backend
    'social_core.backends.open_id.OpenIdAuth',  # Optional OpenId backend
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

SOCIAL_AUTH_STEAM_API_KEY = os.getenv('STEAM_API_KEY')  # Set the Steam API key

SOCIAL_ACCOUNT_PROVIDERS = {
    'steam': {
        'SCOPE': ['user_friends'],  # Permissions you want to request
        'VERIFIED_EMAIL': True  # Ensures email verification
    }
}

