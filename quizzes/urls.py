from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^quizzes/$', 'quizzes.views.index', name='index'),
    url(r'^quizzes/create/$', 'quizzes.views.create', name='create'),
    url(r'^quizzes/edit/$', 'quizzes.views.edit_quizzes', name='edit')
)

urlpatterns += patterns(
    '',
    url(r'quiz/(?P<quiz_id>\d+)/edit/$',
        'quizzes.views.edit_quiz',
        name='edit_quiz'),
    url(r'quiz/(?P<quiz_id>\d+)/delete/$',
        'quizzes.views.delete_quiz',
        name='delete_quiz'),
    url(r'quiz/(?P<quiz_id>\d+)/article/edit/$',
        'quizzes.views.edit_article',
        name='edit_article'),
    url(r'quiz/(?P<quiz_id>\d+)/questions/edit/$',
        'quizzes.views.edit_questions',
        name='edit_questions'),
    url(r'quiz/(?P<quiz_id>\d+)/attempt/$',
        'quizzes.views.attempt',
        name='attempt')
)
