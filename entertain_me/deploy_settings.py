__author__ = 'anmekin'

from settings import *

SECRET_KEY = 'vro=eb!5^-_7^2373ii2tc)g5sad_&%oe=$mnk^h7apgbodia+'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'djangouser',
        'OPTIONS': {'charset': 'utf8mb4'},
        'PASSWORD': '888968',
        'HOST': '',
        'PORT': '',
    }
}

SOCIAL_AUTH_FLICKR_KEY = '345f75b44303f45dd5356ee57b54df81'
SOCIAL_AUTH_FLICKR_SECRET = '90aef24a6b3558ed'
SOCIAL_AUTH_FLICKR_AUTH_EXTRA_ARGUMENTS = {'perms':'read'}
