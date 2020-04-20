from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from .models import Tag, Question


def create_sample_user(email='test@example.com'):
    return get_user_model().objects.create_user(email=email, password='testpass')


def create_sample_question(user, title='sample_title', text='sample_text'):
    return Question.objects.create(user=user, title=title, text=text)


class TagModelTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(TagModelTests, self).__init__(*args, **kwargs)
        self.test_name = 'testTag'

    def test_tag_str(self):
        tag = Tag.objects.create(name=self.test_name)
        self.assertEqual(self.test_name, str(tag))


class QuestionPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_questions_list_page(self):
        resp = self.client.get(reverse('action:question-list'))
        self.assertEqual(resp.status_code, 200)


class PublicQuestionCreateTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_create_question_page(self):
        """If user is not logged in, should be redirected to login page"""
        resp = self.client.get(reverse('action:question-create'))
        self.assertEqual(resp.status_code, 302)


class PrivateQuestionCreateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_sample_user()
        self.client.force_login(self.user)

    def test_get_create_question_page(self):
        """If user is logged in, should return 200 OK"""
        resp = self.client.get(reverse('action:question-create'))
        self.assertEqual(resp.status_code, 200)

    def test_create_question(self):
        """After successful creation of a question, should redirect to questions page"""
        payload = {
            'title': 'test_title',
            'text': 'test_text'
        }
        resp = self.client.post(reverse('action:question-create'), payload)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get(id=1).title, payload['title'])
        self.assertEqual(Question.objects.get(id=1).text, payload['text'])


class PublicQuestionUpdateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_sample_user()
        self.client.force_login(self.user)

    def test_retrieve_update_with_not_creator_user(self):
        question = create_sample_question(
            user=create_sample_user('another_email@example.com'))
        resp = self.client.get(
            reverse('action:question-edit', kwargs={'pk': '{}'.format(question.id)}))
        self.assertEqual(resp.status_code, 403)

    def test_delete_with_not_creator_user(self):
        question = create_sample_question(
            user=create_sample_user('another_email@example.com'))
        resp = self.client.get(
            reverse('action:question-delete', kwargs={'pk': '{}'.format(question.id)}))
        self.assertEqual(resp.status_code, 403)


class PrivateQuestionUpdateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_sample_user()
        self.client.force_login(self.user)

    def test_retrieve_update_question_correct_user(self):
        question = create_sample_question(user=self.user)
        resp = self.client.get(
            reverse('action:question-edit', kwargs={'pk': '{}'.format(question.id)}))
        self.assertEqual(resp.status_code, 200)

    def test_update_question_correct_user(self):
        question = create_sample_question(user=self.user)
        payload = {
            'title': 'new_title',
            'text': 'new_text'
        }
        resp = self.client.post(
            reverse('action:question-edit', kwargs={'pk': '{}'.format(question.id)}), payload)
        self.assertEqual(resp.status_code, 302)
        question.refresh_from_db()
        self.assertEqual(question.title, 'new_title')
        self.assertEqual(question.text, 'new_text')

    def test_delete_question_correct_user(self):
        question = create_sample_question(user=self.user)
        resp = self.client.delete(
            reverse('action:question-delete', kwargs={'pk': '{}'.format(question.id)}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Question.objects.count(), 0)
