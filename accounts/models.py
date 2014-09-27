from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
