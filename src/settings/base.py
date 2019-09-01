"""
Django settings for apps project.

Generated by 'django-admin startproject' using Django 1.11.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-)!o3=yy^i5hu-kqx8-4$txawsz5krycf^gx9lboj3pw3)e^)!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'django_crontab',
    'apps.device',
    'apps.task'
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

ROOT_URLCONF = 'apps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'settings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

SITE_DIR = os.path.dirname(BASE_DIR)

# log
LOGS_DIR = os.path.join(SITE_DIR, "logs")
LOGS_FILE_ROOT = os.path.join(LOGS_DIR, "root.log")
info_file_name = os.path.join(LOGS_DIR, "info.log")
warning_file_name = os.path.join(LOGS_DIR, "warning.log")

BYTES_SIZE_100M = 100 * 1024 * 1024
BYTES_SIZE_1G = 1024 * 1024 * 1024
LOG_BACKUP_CNT = 90
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'common': {
            'format': u'%(asctime)s | pid=%(process)d | thid=%(thread)d | %(levelname)s | %(module)s | %(message)s'
        },
        'simple': {
            'format': u'%(asctime)s | %(message)s'
        },
    },
    'handlers': {

        'root_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGS_FILE_ROOT,
            'formatter': 'common',
            'when': 'MIDNIGHT',
            'backupCount': LOG_BACKUP_CNT,
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': info_file_name,
            'formatter': 'common',
            'when': 'MIDNIGHT',
            'backupCount': LOG_BACKUP_CNT,
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': warning_file_name,
            'formatter': 'common',
            'when': 'MIDNIGHT',
            'backupCount': LOG_BACKUP_CNT,
        },

    },
    'loggers': {
        'info_log': {
            'handlers': ['info_file'],
            'level': 'INFO',
        },
        'warning_log': {
            'handlers': ['warning_file'],
            'level': 'WARNING',
        },
        '': {
            'handlers': ['root_file'],
            'level': 'DEBUG',
        }
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
APPEND_SLASH = True
STATIC_URL = '/backend/static/'

STATIC_ROOT = os.path.normpath(os.path.join(SITE_DIR, 'assets'))
PHONE_HEARTBEAT_TIMEOUT = 60
SLAVE_HEARTBEAT_TIMEOUT = 90
RUN_SCHEDULE_TIMEOUT = 10
