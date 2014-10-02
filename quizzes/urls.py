from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^quizzes/create/$', 'quizzes.views.create', name='create')
)

urlpatterns += patterns(
    '',
    url(r'quiz/(?P<quiz_id>\d+)/attempt/$',
        'quizzes.views.attempt',
        name='attempt')
)
