from django.db import models

from accounts.models import Profile


class Course(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, null=True)
    long_description = models.TextField(null=True)
    owner = models.ForeignKey(Profile)
    instructors = models.ManyToManyField(Profile, related_name='instructor_in')
    assistants = models.ManyToManyField(Profile, related_name='assistant_in')
    students = models.ManyToManyField(Profile, related_name='student_in')
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
