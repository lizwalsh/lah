"""
Django settings for lah project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# for windows
import os.path

from lah.settings_keys import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'lah',
    'ckeditor',
    'photologue',
    'sortedm2m',
    'twython_django_oauth',
    'comics.apps.ComicsConfig',
    'cast.apps.CastConfig',
    'news.apps.NewsConfig',
    'archive.apps.ArchiveConfig',
    'about.apps.AboutConfig',
    'extras.apps.ExtrasConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = 1

ROOT_URLCONF = 'lah.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'comics.ccr.site',
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ],
            # got this from python anti-pattern - take out if it doesn't work
            #'loaders': [
            #    'django.template.loaders.filesystem.Loader',
            #    'django.template.loaders.app_directories.Loader',
            #],       
        },
    },
]


WSGI_APPLICATION = 'lah.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC-5'
TIME_ZONE = "US/Eastern"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATIC_ROOT = '/home/litazia/lah/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, 'static')
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Media files (uploads)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_ROOT = '/home/litazia/lah/media/'
MEDIA_URL = '/media/'

# define some variables for myself
SITE_URL = 'http://www.lifesahowl.com/'


# comics folder
#COMICS_ROOT = os.path.join(MEDIA_ROOT, '/comix')
COMICS_ROOT = os.path.join(BASE_DIR, 'media/comix')
COMICS_URL = '/media/comix/'
COMICS_F = 'comix'

#UPLOAD_ROOT = os.path.join(MEDIA_ROOT, '/uploads')
UPLOAD_ROOT = os.path.join(BASE_DIR, 'media/uploads')
UPLOAD_F = 'uploads'

#PREVIEW_ROOT = os.path.join(BASE_DIR, '/preview')
PREVIEW_ROOT = os.path.join(BASE_DIR, 'media/preview')
PREVIEW_URL = '/media/preview/'

LOGIN_URL = ''
LOGOUT_URL = ''
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
