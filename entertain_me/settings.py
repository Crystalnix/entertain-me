"""
Django settings for entertain_me project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

SECRET_KEY = 'vro=eb!5^-_7^2373ii2tc)g5sad_&%oe=$mnk^h7apgbodia+'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'social.apps.django_app.default',
    'djcelery',
    'debug_toolbar',
    'django_nose',
    'compressor',
    'raven.contrib.django.raven_compat'
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'entertain_me.urls'

WSGI_APPLICATION = 'entertain_me.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    'compressor.finders.CompressorFinder',
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

LOGIN_URL = '/auth/'

# Social_autth
SOCIAL_AUTH_FLICKR_KEY = ''
SOCIAL_AUTH_FLICKR_SECRET = ''
SOCIAL_AUTH_FLICKR_AUTH_EXTRA_ARGUMENTS = {}

SOCIAL_AUTH_LOGIN_URL = '/login-form/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/oauth_callback/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'


AUTHENTICATION_BACKENDS = (
    'social.backends.flickr.FlickrOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)


# Celery
import djcelery

from datetime import timedelta
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_IMPORTS = ("app",)
CELERYBEAT_SCHEDULE = {
    'update_user': {
        'task': 'tasks.update_flickr_user',
        'schedule': timedelta(seconds=2),
    },
    'update_photo': {
        'task': 'tasks.update_photo',
        'schedule': timedelta(seconds=2),
    },
}

CELERY_TIMEZONE = 'UTC'

# django_debug_toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ('127.0.0.1',)

# nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=app',
    '--cover-html',
]

# compressor
COMPRESS_ENABLED = False
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
)

#

#Sentry & raven
#SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'

RAVEN_CONFIG = {
    'dsn':'https://d0cc19623fb64c5eb4c3f3694a20b279:a7228f01811f4ba093c9f7ce23fed2b0@app.getsentry.com/40353',
}


try:
    from local_settings import *
except ImportError:
    pass
