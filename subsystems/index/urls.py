from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^test/$', test),
    url(r'^question/$', question),
)