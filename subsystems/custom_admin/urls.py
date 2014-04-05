from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^statistic/$', statistic),
    url(r'^test_question/$', test_question),  # ajax
    # url(r'^user_action/$', user_action),  # ajax
)