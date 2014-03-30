from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^tests/$', test),
    url(r'^question/$', question),
    url(r'^answer/$', answer),
    url(r'^password_restore/$', password_restore),
    url(r'^password_restore_confirm/$', password_restore_confirm),
)