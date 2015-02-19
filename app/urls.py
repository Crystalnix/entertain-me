__author__ = 'anmekin'

from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

urlpatterns = patterns('',
    # Examples:
    url(r'^auth$', auth, name='auth'),
    url(r'^my_auth$', my_auth, name='my_auth'),
    url(r'^oauth_callback$', oauth_callback, name='oauth_callback'),

)
