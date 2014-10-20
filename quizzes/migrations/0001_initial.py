# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('correct', models.NullBooleanField()),
                ('answer', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('submitted', models.BooleanField(default=False)),
                ('scored', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to='accounts.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('source_url', models.URLField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ManyToManyField(to='accounts.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('question', models.CharField(max_length=100)),
                ('standard_answer', models.CharField(null=True, max_length=100)),
                ('sequence', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('sequence',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('due', models.DateTimeField(null=True)),
                ('article', models.OneToOneField(null=True, to='quizzes.Article')),
                ('assigned_to', models.ManyToManyField(to='accounts.Profile')),
                ('course', models.ForeignKey(to='courses.Course')),
                ('owner', models.ForeignKey(to='accounts.Profile', related_name='created_quizzes')),
            ],
            options={
                'permissions': (('edit_quiz', 'Edit quiz'), ('attempt_quiz', 'Attempt quiz')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(to='quizzes.Quiz', related_name='questions'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answersheet',
            name='quiz',
            field=models.ForeignKey(to='quizzes.Quiz'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_sheet',
            field=models.ForeignKey(to='quizzes.AnswerSheet', related_name='answers'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='quizzes.Question'),
            preserve_default=True,
        ),
    ]
