from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^courses/open/$', 'courses.views.open_course', name='open')
)

urlpatterns += patterns(
    '',
    url(r'course/(?P<course_id>\d+)/edit/$', 'courses.views.edit', name='edit')
)