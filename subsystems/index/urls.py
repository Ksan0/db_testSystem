from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^tests/$', test),
    url(r'^question/$', question),
    url(r'^test_answer/$', test_answer),
    url(r'^close_session/$', close_session),
    url(r'^password_restore/$', password_restore),
    url(r'^password_restore_confirm/$', password_restore_confirm),
)