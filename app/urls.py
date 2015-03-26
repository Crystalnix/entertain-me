__author__ = 'anmekin'

from django.conf.urls import patterns, url
from views import *
from ajax import *

urlpatterns = patterns('',
                       url(r'^$', recommended, name='home'),
                       url(r'^like/$', like, name='like'),
                       url(r'^auth/$', auth, name='auth'),
                       url(r'^update/$', update, name='update'),
                       url(r'^test/$', test, name='test'),
                       url(r'^logout/$', logout, name='logout'),
                       url(r'^bad_request/$', test_exception, name='test_exception'),
                       url(r'^oauth_callback/$', oauth_callback, name='oauth_callback'),
                       )
