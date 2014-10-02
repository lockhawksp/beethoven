from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework import generics, mixins

from quizzes.models import Article
from quizzes.serializers import ArticleSerializer


@login_required
def create(request):
    pass


@login_required
def attempt(request, quiz_id):
    context = {'quiz_id': quiz_id}
    return render(request, 'quizzes/attempt.html', context)


class ArticleDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
