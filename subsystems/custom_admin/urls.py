from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^user/$', user_stats),
    url(r'^statistic/$', statistic),
)