from django.conf.urls import patterns, url

from quizzes.views import ArticleDetails


urlpatterns = patterns(
    '',
    url(r'^quizzes/articles/(?P<pk>\d+)/$',
        ArticleDetails.as_view(),
        name='article_details')
)
