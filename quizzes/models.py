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
    article = models.OneToOneField(Article, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due = models.DateTimeField(null=True)
    owner = models.ForeignKey(Profile, related_name='created_quizzes')
    assigned_to = models.ManyToManyField(Profile)

    class Meta(object):
        permissions = (
            ('edit_quiz', 'Edit quiz'),
            ('attempt_quiz', 'Attempt quiz')
        )

    def __str__(self):
        return str(self.pk)


class AnswerSheet(models.Model):
    quiz = models.ForeignKey(Quiz)
    owner = models.ForeignKey(Profile)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted = models.BooleanField(default=False)
    scored = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions')
    question = models.CharField(max_length=100)
    standard_answer = models.CharField(max_length=100)
    sequence = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ('sequence',)

    def __str__(self):
        return self.question


class Answer(models.Model):
    # Staff only
    answer_sheet = models.ForeignKey(AnswerSheet, related_name='answers')
    question = models.ForeignKey(Question)
    correct = models.NullBooleanField(null=True)

    # Student only
    answer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer
