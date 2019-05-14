import datetime
import os

from .secret_settings import *


if SERVER == 'LOCAL':
    DEBUG = True
    HOST = 'http://localhost:8000'
    PROJECT_PATH = '/Users/Andrew/w_projects/asphere/'
    logs_file = '/Users/Andrew/w_projects/test/logs/logs.log'
    request_logs_file = '/Users/Andrew/w_projects/test/logs/django_request.log'
    cron_logs_file = '/Users/Andrew/w_projects/test/logs/cron.log'
else:
    DEBUG = True
    HOST = 'http://asphere.online'
    PROJECT_PATH = '/root/asphere/'
    logs_file = '/root/test/logs/server_logs.log'
    request_logs_file = '/root/test/logs/server_django_request.log'
    cron_logs_file = '/root/test/logs/server_cron.log'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_framework_jwt',
    'app1_accounts',
    'app2_notebooks',

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


ROOT_URLCONF = 'main_files.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {

            }
        },
    },
]

WSGI_APPLICATION = 'main_files.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



AUTH_USER_MODEL = 'app1_accounts.User'


AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',

    ),
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    # )
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    )
}
