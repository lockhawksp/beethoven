# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('short_description', models.CharField(null=True, max_length=200)),
                ('long_description', models.TextField(null=True)),
                ('start', models.DateField(null=True)),
                ('end', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assistants', models.ManyToManyField(to='accounts.Profile', related_name='assistant_in')),
                ('instructors', models.ManyToManyField(to='accounts.Profile', related_name='instructor_in')),
                ('owner', models.ForeignKey(to='accounts.Profile')),
                ('students', models.ManyToManyField(to='accounts.Profile', related_name='student_in')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
