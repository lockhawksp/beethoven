from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'beethoven.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('allauth.urls'))
)
