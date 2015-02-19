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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vro=eb!5^-_7^2373ii2tc)g5sad_&%oe=$mnk^h7apgbodia+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

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
    'flickrapi',
    #'social_auth',
)

MIDDLEWARE_CLASSES = (
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

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

#
# FLICKR_APP_ID = '345f75b44303f45dd5356ee57b54df81'
# FLICKR_API_SECRET = '90aef24a6b3558ed'
#
# LOGIN_URL          = '/login-form/'
# LOGIN_REDIRECT_URL = '/logged-in/'
# LOGIN_ERROR_URL    = '/login-error/'
#
# AUTHENTICATION_BACKENDS = (
#     'social_auth.backends.twitter.TwitterBackend',
#     'social_auth.backends.facebook.FacebookBackend',
#     'social_auth.backends.google.GoogleOAuthBackend',
#     'social_auth.backends.google.GoogleOAuth2Backend',
#     'social_auth.backends.google.GoogleBackend',
#     'social_auth.backends.yahoo.YahooBackend',
#     'social_auth.backends.browserid.BrowserIDBackend',
#     'social_auth.backends.contrib.linkedin.LinkedinBackend',
#     'social_auth.backends.contrib.disqus.DisqusBackend',
#     'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#     'social_auth.backends.contrib.orkut.OrkutBackend',
#     'social_auth.backends.contrib.foursquare.FoursquareBackend',
#     'social_auth.backends.contrib.github.GithubBackend',
#     'social_auth.backends.contrib.vk.VKOAuth2Backend',
#     'social_auth.backends.contrib.live.LiveBackend',
#     'social_auth.backends.contrib.skyrock.SkyrockBackend',
#     'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
#     'social_auth.backends.contrib.readability.ReadabilityBackend',
#     'social_auth.backends.contrib.fedora.FedoraBackend',
#     'social_auth.backends.OpenIDBackend',
#     'social_auth.backends.contrib.flickr',
#     'django.contrib.auth.backends.ModelBackend',
# )

api_key = u'345f75b44303f45dd5356ee57b54df81'
api_secret = u'90aef24a6b3558ed'