from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import generics, mixins

from courses.models import Course
from quizzes.models import Article, Quiz
from quizzes.serializers import (ArticleSerializer,
                                 QuizSerializer)
from quizzes.services import create_meta_quiz


@login_required
def create(request):
    if request.method == 'GET':
        p = request.user.profile
        courses = p.instructor_in.all()
        context = {'courses': courses}
        return render(request, 'quizzes/create.html', context)

    else:
        course_id = int(request.POST['course'])
        course = get_object_or_404(Course, pk=course_id)
        meta_quiz = create_meta_quiz(course)
        kwargs = {'quiz_id': meta_quiz.id}
        return redirect(reverse('quizzes:edit_article', kwargs=kwargs))


@login_required
def edit_article(request, quiz_id):
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


class QuizDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
