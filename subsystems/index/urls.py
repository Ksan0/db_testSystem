from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),  # no GUI
    url(r'^tests/$', test),
    url(r'^question/$', question),
    url(r'^test_answer/$', test_answer),  # ajax
    url(r'^close_session/$', close_session),  # no GUI
    url(r'^password_restore/$', password_restore),  # no GUI
    url(r'^password_restore_confirm/$', password_restore_confirm),  # no GUI
)