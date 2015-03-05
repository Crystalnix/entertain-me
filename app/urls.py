__author__ = 'anmekin'

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
                       url(r'^$', home, name='home'),
                       url(r'^test/$', recomended, name='recomended'),
                       url(r'^testa', test_ajax, name='test_ajax'),
                       url(r'^photos', show_photos, name='show_fotos'),
                       url(r'^logout', logout, name='logout'),
                       url(r'^auth$', auth, name='auth'),
                       url(r'^oauth_callback', oauth_callback, name='oauth_callback'),
                       )
