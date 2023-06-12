from pathlib import Path
import os

from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost', 'web']

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

CUSTOM_APPS = [
    'apps.member.apps.MembersConfig',
    'apps.poll.apps.PollsConfig',
    'apps.user_profile.apps.UserProfileConfig',
    'apps.company.apps.CompanyConfig',
    'apps.office.apps.OfficeConfig',
    'apps.worker.apps.WorkerConfig',
    'apps.vehicle.apps.VehicleConfig',
    'apps.verification_token.apps.VerificationTokenConfig',
    'apps.audit.apps.AuditConfig',
]

EXTERNAL_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'channels',
]

INSTALLED_APPS = DEFAULT_APPS + CUSTOM_APPS + EXTERNAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

WSGI_APPLICATION = 'mysite.wsgi.application'

ROOT_URLCONF = 'mysite.urls'

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

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('MAIN_ENGINE'),
        'NAME': os.environ.get('MAIN_DB'),
        'USER': os.environ.get('MAIN_USER'),
        'PASSWORD': os.environ.get('MAIN_PASSWORD'),
        'HOST': os.environ.get('MAIN_HOST'),
        'PORT': os.environ.get('MAIN_PORT'),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user_profile.UserProfile'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

SITE_ID=1

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND')

ASGI_APPLICATION = "mysite.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

CELERY_BEAT_SCHEDULE = {
    'calculate-vehicles-number': {
        'task': 'apps.vehicle.tasks.calculate_vehicles_number',
        'schedule': crontab(hour='*/1')
    },
    'send-vehicle-report': {
        'task': 'apps.vehicle.tasks.send_vehicle_report',
        'schedule': crontab(day_of_week='friday', hour='20')
    },
}
