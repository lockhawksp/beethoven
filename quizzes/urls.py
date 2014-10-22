from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^quizzes/$', 'quizzes.views.index', name='index'),
    url(r'^quizzes/create/$', 'quizzes.views.create', name='create'),
    url(r'^quizzes/edit/$', 'quizzes.views.edit_quizzes', name='edit'),
    url(r'^quizzes/new_assignments/$',
        'quizzes.views.new_assignments',
        name='new_assignments'),
    url(r'^quizzes/done_assignments/$',
        'quizzes.views.done_assignments',
        name='done_assignments')
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
    url(r'quiz/(?P<quiz_id>\d+)/solutions/edit/$',
        'quizzes.views.edit_solutions',
        name='edit_solutions'),
    url(r'quiz/(?P<quiz_id>\d+)/attempt/$',
        'quizzes.views.attempt',
        name='attempt')
)
