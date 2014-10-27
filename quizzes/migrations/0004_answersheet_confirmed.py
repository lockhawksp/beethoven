# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0003_quiz_solution_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='answersheet',
            name='confirmed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
