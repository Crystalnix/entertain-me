__author__ = 'anmekin'

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
                       url(r'^$', home, name='home'),
                       url(r'^test/$', recommended, name='recommended'),
                       url(r'^photos', show_photos, name='show_fotos'),
                       url(r'^logout', logout, name='logout'),
                       url(r'^auth$', auth, name='auth'),
                       url(r'^oauth_callback', oauth_callback, name='oauth_callback'),
                       )
