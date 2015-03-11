__author__ = 'anmekin'

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
                       url(r'^$', home, name='home'),
                       url(r'^get_photo/$', recommended, name='recommended'),
                       url(r'^logout', logout, name='logout'),
                       url(r'^oauth_callback', oauth_callback, name='oauth_callback'),
                       )
