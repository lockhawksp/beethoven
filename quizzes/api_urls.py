from django.conf.urls import patterns, url

from quizzes.views import ArticleDetails, QuizDetails


urlpatterns = patterns(
    '',
    url(r'^quizzes/articles/(?P<pk>\d+)/$',
        ArticleDetails.as_view(),
        name='article_details'),
    url(r'^quizzes/(?P<pk>\d+)/$',
        QuizDetails.as_view(),
        name='quiz_details')
)
