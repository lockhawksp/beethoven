import json

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import generics, mixins

from guardian.shortcuts import get_objects_for_user

from courses.models import Course
from quizzes.models import Article, Quiz, AnswerSheet
from quizzes.serializers import (ArticleSerializer,
                                 QuizSerializer,
                                 AnswerSheetSerializer)
from quizzes.services import (create_quiz,
                              create_article,
                              update_questions,
                              create_answer_sheet,
                              update_answers,
                              is_due)
from quizzes.forms import EditArticleForm
from quizzes.queries import find_new_assignments, find_done_assignments


@login_required
def create(request):
    p = request.user.profile

    if request.method == 'GET':
        courses = p.instructor_in.all()
        context = {'courses': courses}
        return render(request, 'quizzes/create.html', context)

    else:
        course_id = int(request.POST['course'])
        course = get_object_or_404(Course, pk=course_id)
        quiz = create_quiz(p, course)
        kwargs = {'quiz_id': quiz.id}
        return redirect(reverse('quizzes:edit_article', kwargs=kwargs))


@login_required
def edit_quizzes(request):
    if request.method == 'GET':
        quizzes = get_objects_for_user(request.user, 'edit_quiz', klass=Quiz)
        context = {'quizzes': quizzes}
        return render(request, 'quizzes/edit_quizzes.html', context)


@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'GET':
        context = {'course': quiz.course, 'quiz_id': quiz_id}
        return render(request, 'quizzes/edit_quiz.html', context)

    else:
        kwargs = {'quiz_id': quiz.id}
        return redirect(reverse('quizzes:edit_article', kwargs=kwargs))


@login_required
def edit_article(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'GET':
        context = {'quiz': quiz}
        return render(request, 'quizzes/edit_article.html', context)

    else:
        form = EditArticleForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            source_url = form.cleaned_data['source_url']
            content = form.cleaned_data['content']
            create_article(quiz, title, content, source_url)

            kwargs = {'quiz_id': quiz_id}
            return redirect(reverse('quizzes:edit_questions', kwargs=kwargs))

        else:
            context = {
                'quiz_id': quiz_id,
                'errors': []
            }

            errors = context['errors']
            for field in form:
                if field.errors:
                    errors.extend(field.errors)
                else:
                    context[field.name] = field.data

            return render(request, 'quizzes/edit_article.html', context)


@login_required
def edit_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'GET':
        context = {'quiz_id': quiz_id}
        return render(request, 'quizzes/edit_questions.html', context)

    else:
        if 'questions' not in request.POST:
            context = {
                'quiz_id': quiz_id,
                'errors': ['Invalid data.']
            }
            return render(request, 'quizzes/edit_questions.html', context)

        new_questions = json.loads(request.POST['questions'])
        update_questions(quiz, new_questions)
        return redirect(reverse('quizzes:index'))


@login_required
def index(request):
    if request.method == 'GET':
        return render(request, 'quizzes/index.html')


@login_required
def new_assignments(request):
    if request.method == 'GET':
        p = request.user.profile
        quizzes = find_new_assignments(p)
        context = {'quizzes': quizzes}
        return render(request, 'quizzes/new_assignments.html', context)


@login_required
def done_assignments(request):
    if request.method == 'GET':
        p = request.user.profile
        quizzes = find_done_assignments(p)
        context = {'quizzes': quizzes}
        return render(request, 'quizzes/new_assignments.html', context)


@login_required
def attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    u = request.user
    p = u.profile

    due_error = 'This assignment is due. You cannot edit it.'

    if not u.has_perm('attempt_quiz', quiz):
        return HttpResponseForbidden()

    if request.method == 'GET':
        if is_due(quiz):
            context = {'error': due_error}
            return render(request, 'quizzes/error.html', context)

        try:
            answer_sheet = AnswerSheet.objects.get(quiz=quiz, owner=p)
        except AnswerSheet.DoesNotExist:
            answer_sheet = None

        if answer_sheet is None:
            answer_sheet = create_answer_sheet(p, quiz)

        context = {'quiz_id': quiz_id, 'answer_sheet': answer_sheet}
        return render(request, 'quizzes/attempt.html', context)

    else:
        if is_due(quiz):
            return JsonResponse({'error': due_error})

        data = json.loads(request.body.decode('utf-8'))

        if 'answers' not in data:
            context = {
                'quiz_id': quiz_id,
                'errors': ['Invalid data.']
            }
            return render(request, 'quizzes/attempt.html', context)

        update_answers(data['answers'])

        answer_sheet = AnswerSheet.objects.get(owner=p, quiz=quiz)
        answer_sheet.submitted = True
        answer_sheet.save()

        return JsonResponse({
            'msg': 'answers saved.',
            'next': reverse('quizzes:index')
        })


@login_required
def delete_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        if request.user.has_perm('delete_quiz', quiz):
            quiz.delete()
            return JsonResponse({'msg': 'deleted'})
        else:
            return HttpResponseForbidden()


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


class AnswerSheetDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = AnswerSheet.objects.all()
    serializer_class = AnswerSheetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
