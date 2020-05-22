from django.shortcuts import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model


def create_sample_user(email='test@example.com'):
    return get_user_model().objects.create_user(email=email, password='testpass')


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

class PublicUserEditTests(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()
    
    def test_access_edit_page_anonymous(self):
        """if user is not logged in, redirect to login page"""
        resp = self.client.get(reverse('user:edit'))
        self.assertEqual(resp.status_code, 302)
    
    def test_access_change_pass_page_anonymous(self):
        """if user is not logged in, redirect to login page"""
        resp = self.client.get(reverse('user:changepass'))
        self.assertEqual(resp.status_code, 302)


class PrivateUserEditTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_sample_user()
        self.client.force_login(self.user)
        return super().setUp()
    
    def test_update_user(self):
        name = 'test_name'
        payload = {
            'name': name,
            'email': 'test_email@example.com'
        }
        resp = self.client.post(reverse('user:edit'), payload)
        self.assertEqual(resp.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, name)

    def test_change_user_pass(self):
        new_password = 'test_name'
        payload = {
            'old_password' : 'testpass',
            'new_password1': new_password,
            'new_password2': new_password
        }
        resp = self.client.post(reverse('user:changepass'), payload)
        self.assertEqual(resp.status_code, 302)
        self.user.refresh_from_db()
        self.user.check_password(new_password)
