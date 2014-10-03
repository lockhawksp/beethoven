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


class MetaQuiz(models.Model):
    course = models.ForeignKey(Course)
    article = models.ForeignKey(Article, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due = models.DateTimeField(null=True)
    # created_by = models.ManyToManyField(
    #     Profile, related_name='created_quizzes'
    # )

    def __str__(self):
        return self.pk


class Quiz(models.Model):
    # Staff only
    course = models.ForeignKey(Course)
    article = models.ForeignKey(Article)
    meta_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    assigned_to = models.ForeignKey(Profile)
    due = models.DateTimeField(null=True)
    created_by = models.ManyToManyField(
        Profile, related_name='created_quizzes'
    )
    scored = models.BooleanField(default=False)

    # Student only
    attempted = models.BooleanField(default=False)
    last_attempt = models.DateTimeField(null=True)

    def __str__(self):
        return self.pk


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
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    correct = models.NullBooleanField(null=True)

    # Student only
    answer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer
