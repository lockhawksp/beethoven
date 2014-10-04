from django.db import models

from accounts.models import Profile
from courses.models import Course


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    source_url = models.URLField(null=True)
    created_by = models.ManyToManyField(Profile)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    course = models.ForeignKey(Course)
    article = models.ForeignKey(Article, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due = models.DateTimeField(null=True)
    # created_by = models.ManyToManyField(
    #     Profile, related_name='created_quizzes'
    # )

    def __str__(self):
        return str(self.pk)


class AnswerSheet(models.Model):
    quiz = models.ForeignKey(Quiz)
    assigned_to = models.ForeignKey(Profile)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scored = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions')
    question = models.CharField(max_length=100)
    standard_answer = models.CharField(max_length=100, null=True)
    sequence = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    # Staff only
    answer_sheet = models.ForeignKey(AnswerSheet)
    question = models.ForeignKey(Question)
    correct = models.NullBooleanField(null=True)

    # Student only
    answer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer
