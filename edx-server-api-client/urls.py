from django.conf.urls import patterns, include, url
from django.conf import settings

if settings.RUN_LOCAL_MOCK_API:
    urlpatterns += patterns('', url(r'^mockapi/', include('mockapi.urls'), name='mockapi'), )
