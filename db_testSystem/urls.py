from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'db_testSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('subsystems.index.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^custom-admin/', include('subsystems.custom_admin.urls'))
)
