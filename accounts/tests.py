from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile


class AccountTests(TestCase):

    def setUp(self):
        User.objects.create_user('user', password='0')

    def test_profile_is_created_after_user_is_created(self):
        Profile.objects.get(user__username='user')
