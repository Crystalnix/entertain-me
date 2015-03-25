from settings import *

SECRET_KEY = 'YOUR_KEY'

ALLOWED_HOSTS = [
	'*',
]
ALLOWED_INCLUDE_ROOTS = (
	'/path/to/entertain-me',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS += ('gunicorn',)

USE_X_FORWARDED_HOST = True

#social_auth

SOCIAL_AUTH_FLICKR_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
SOCIAL_AUTH_FLICKR_SECRET = 'XXXXXXXXXXXXXXXX'
SOCIAL_AUTH_FLICKR_AUTH_EXTRA_ARGUMENTS = {'perms':'read'}
