from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
