from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(UserModelTests, self).__init__(*args, **kwargs)
        self.test_email = 'foobar@example.com'
        self.test_password = 'foopass'

    def test_create_user(self):
        """ Test creating a normal user"""

        User = get_user_model()
        user = User.objects.create_user(
            email=self.test_email, password=self.test_password)
        self.assertEqual(user.email, self.test_email)
        self.assertTrue(user.check_password(self.test_password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """ Test creating a user wit admin privileges """
        User = get_user_model()
        user = User.objects.create_superuser(
            email=self.test_email, password=self.test_password)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
