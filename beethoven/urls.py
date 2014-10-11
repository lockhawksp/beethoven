from django.conf.urls import patterns, include, url
from django.contrib import admin

from beethoven import settings


urlpatterns = patterns(
    '',
    url(r'^$', 'beethoven.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('allauth.urls')),
    url(r'^', include('courses.urls', namespace='courses')),
    url(r'^', include('quizzes.urls', namespace='quizzes')),
    url(r'^api/', include('quizzes.api_urls', namespace='quizzes_api'))
)

if settings.PRODUCTION:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT})
    )
