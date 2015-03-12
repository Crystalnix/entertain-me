__author__ = 'anmekin'

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
                       url(r'^$', recommended, name='home'),
                       url(r'^auth/$', auth, name='auth'),
                       url(r'^logout/$', logout, name='logout'),
                       url(r'^oauth_callback/$', oauth_callback, name='oauth_callback'),
                       )
