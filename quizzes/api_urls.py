from django.conf.urls import patterns, url

from quizzes.views import ArticleDetails, QuizDetails, AnswerSheetDetails


urlpatterns = patterns(
    '',
    url(r'^quizzes/articles/(?P<pk>\d+)/$',
        ArticleDetails.as_view(),
        name='article_details'),
    url(r'^quizzes/(?P<pk>\d+)/$',
        QuizDetails.as_view(),
        name='quiz_details'),
    url(r'^quizzes/answer_sheets/(?P<pk>\d+)/$',
        AnswerSheetDetails.as_view(),
        name='answer_sheet_details')
)
