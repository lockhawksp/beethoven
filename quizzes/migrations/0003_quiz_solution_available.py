# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_auto_20141026_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='solution_available',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
