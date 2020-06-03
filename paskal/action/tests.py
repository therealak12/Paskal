from unittest import skipIf
import time

from django.urls import reverse
from django.conf import settings
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model

from .models import Question

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from taggit.models import Tag


def create_sample_user(email='test@example.com'):
    return get_user_model().objects.create_user(email=email, password='testpass')


def create_sample_question(user, title='sample_title', text='sample_text', tags=[]):
    question = Question.objects.create(user=user, title=title, text=text)
    if len(tags) != 0:
        question.tags.add(*tags)
    return question


# class QuestionPageTests(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_questions_list_page(self):
#         resp = self.client.get(reverse('action:question-list'))
#         self.assertEqual(resp.status_code, 200)


# class PublicQuestionCreateTests(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_get_create_question_page(self):
#         """If user is not logged in, should be redirected to login page"""
#         resp = self.client.get(reverse('action:question-create'))
#         self.assertEqual(resp.status_code, 302)


# class PrivateQuestionCreateTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = create_sample_user()
#         self.client.force_login(self.user)

#     def test_get_create_question_page(self):
#         """If user is logged in, should return 200 OK"""
#         resp = self.client.get(reverse('action:question-create'))
#         self.assertEqual(resp.status_code, 200)

#     def test_create_question(self):
#         """After successful creation of a question, should redirect to questions page"""
#         payload = {
#             'title': 'test_title',
#             'text': 'test_text'
#         }
#         resp = self.client.post(reverse('action:question-create'), payload)
#         self.assertEqual(resp.status_code, 302)
#         self.assertEqual(Question.objects.count(), 1)
#         self.assertEqual(Question.objects.filter()[0].title, payload['title'])
#         self.assertEqual(Question.objects.filter()[0].text, payload['text'])


# class PublicQuestionUpdateTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = create_sample_user()
#         self.client.force_login(self.user)

#     def test_retrieve_update_with_not_creator_user(self):
#         question = create_sample_question(
#             user=create_sample_user('another_email@example.com'))
#         resp = self.client.get(
#             reverse('action:question-edit', kwargs={'pk': '{}'.format(question.id)}))
#         self.assertEqual(resp.status_code, 403)

#     def test_delete_with_not_creator_user(self):
#         question = create_sample_question(
#             user=create_sample_user('another_email@example.com'))
#         resp = self.client.get(
#             reverse('action:question-delete', kwargs={'pk': '{}'.format(question.id)}))
#         self.assertEqual(resp.status_code, 403)


# class PrivateQuestionUpdateTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = create_sample_user()
#         self.client.force_login(self.user)

#     def test_retrieve_update_question_correct_user(self):
#         question = create_sample_question(user=self.user)
#         resp = self.client.get(
#             reverse('action:question-edit', kwargs={'pk': '{}'.format(question.id)}))
#         self.assertEqual(resp.status_code, 200)

#     def test_update_question_correct_user(self):
#         question = create_sample_question(user=self.user)
#         payload = {
#             'title': 'new_title',
#             'text': 'new_text'
#         }
#         resp = self.client.post(
#             reverse('action:question-edit', kwargs={'pk': '{}'.format(question.id)}), payload)
#         self.assertEqual(resp.status_code, 302)
#         question.refresh_from_db()
#         self.assertEqual(question.title, 'new_title')
#         self.assertEqual(question.text, 'new_text')

#     def test_delete_question_correct_user(self):
#         question = create_sample_question(user=self.user)
#         resp = self.client.delete(
#             reverse('action:question-delete', kwargs={'pk': '{}'.format(question.id)}))
#         self.assertEqual(resp.status_code, 302)
#         self.assertEqual(Question.objects.count(), 0)


# class PublicAnswerTests(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_answer_anonymous_user(self):
#         """ The app shouldn't allow an anonymous user to answer a question"""
#         question = create_sample_question(create_sample_user())
#         payload = {
#             'text': 'a text for test'
#         }
#         resp = self.client.post(
#             reverse('action:question-detail', kwargs={'pk': question.id}), payload)
#         self.assertEqual(resp.status_code, 401)


# class PrivateAnswerTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = create_sample_user('pat@example.com')
#         self.client.force_login(self.user)

#     def test_answer_valid_user(self):
#         question = create_sample_question(self.user, 'pat_qtitle')
#         question.refresh_from_db()
#         payload = {
#             'text': 'a text for test'
#         }
#         resp = self.client.post(
#             reverse('action:question-detail', kwargs={'pk': question.id}), payload)
#         self.assertEqual(resp.status_code, 200)


# @skipIf(not getattr(settings, 'SELENIUM_TESTS', False), 'selenium tests are disabled in settings.py')
# class PrivateVoteTests(StaticLiveServerTestCase):

#     def setUp(self):
#         self.user = create_sample_user()
#         self.asking_user = create_sample_user(email='asking@example.com')
#         self.question = create_sample_question(user=self.asking_user)
#         self.own_question = create_sample_question(user=self.user)
#         self.driver = webdriver.Chrome(
#             '/usr/bin/chromedriver')
#         self.driver.maximize_window()
#         self.login_user()
#         super().setUpClass()

#     def login_user(self):
#         client = Client()
#         client.force_login(self.user)
#         cookie = client.cookies['sessionid']
#         self.driver.get(self.live_server_url + '/admin')
#         self.driver.add_cookie(
#             {'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
#         self.driver.refresh()
#         self.driver.get(self.live_server_url + '/admin')

#     def tearDown(self):
#         self.driver.quit()
#         return super().tearDown()

#     def wait_ajax_complete(self):
#         """ Wait until ajax request is completed """
#         WebDriverWait(self.driver, timeout=10).until(
#             lambda s: s.execute_script("return jQuery.active == 0")
#         )

#     def test_vote_up_question(self):
#         """test voting up someone's question"""
#         self.setUpClass()
#         self.driver.get(self.live_server_url + reverse('action:question-detail',
#                                                        kwargs={'pk': self.question.id}))
#         self.driver.find_element_by_id('q_vote_up').click()
#         self.wait_ajax_complete()
#         score = self.driver.find_element_by_id('q_score').text
#         self.assertEqual(score, '1')

#     def check_and_accept_alert(self):
#         try:
#             self.driver.switch_to_alert().accept()
#             return True
#         except:
#             return False

#     def test_vote_up_own_question(self):
#         """user shouldn't be able to vote his/her questions"""
#         self.driver.get(self.live_server_url + reverse('action:question-detail',
#                                                        kwargs={'pk': self.own_question.id}))
#         self.driver.find_element_by_id('q_vote_up').click()
#         self.assertEqual(True, self.check_and_accept_alert())
#         self.assertEqual(self.driver.find_element_by_id('q_score').text, '0')


# @skipIf(not getattr(settings, 'SELENIUM_TESTS', False), 'selenium tests are disabled in settings.py')
# class PublicVoteTests(StaticLiveServerTestCase):
#     """Test anonymous user cannot vote"""

#     def setUp(self):
#         self.user = create_sample_user()
#         self.question = create_sample_question(user=self.user)
#         self.driver = webdriver.Chrome('/usr/bin/chromedriver')
#         self.driver.maximize_window()

#     def tearDown(self):
#         self.driver.quit()
#         return super().tearDown()

#     def check_and_accept_alert(self):
#         try:
#             self.driver.switch_to_alert().accept()
#             return True
#         except:
#             return False

#     def test_anonymous_user_vote_up(self):
#         self.driver.get(self.live_server_url +
#                         reverse('action:question-detail', kwargs={'pk': self.question.id}))
#         self.driver.find_element_by_id('q_vote_up').click()
#         self.assertEqual(True, self.check_and_accept_alert())
#         self.assertEqual(self.driver.find_element_by_id('q_score').text, '0')


# @skipIf(not getattr(settings, 'SELENIUM_TESTS', False), 'selenium tests are disabled in settings.py')
# class PrivateReplyTests(StaticLiveServerTestCase):

#     def setUp(self):
#         self.user = create_sample_user()
#         self.asking_user = create_sample_user(email='asking@example.com')
#         self.question = create_sample_question(user=self.asking_user)
#         self.driver = webdriver.Chrome(
#             '/usr/bin/chromedriver')
#         self.driver.maximize_window()
#         self.login_user()
#         super().setUpClass()

#     def login_user(self):
#         client = Client()
#         client.force_login(self.user)
#         cookie = client.cookies['sessionid']
#         self.driver.get(self.live_server_url + '/admin')
#         self.driver.add_cookie(
#             {'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
#         self.driver.refresh()
#         self.driver.get(self.live_server_url + '/admin')

#     def tearDown(self):
#         self.driver.quit()
#         return super().tearDown()

#     def test_submit_reply(self):
#         """test voting up someone's question"""
#         self.setUpClass()
#         self.driver.get(self.live_server_url + reverse('action:question-detail',
#                                                        kwargs={'pk': self.question.id}))
#         self.driver.find_element_by_id("id_text").send_keys("reply for test")
#         self.driver.find_element_by_name('reply').click()
#         self.assertEqual(self.question.reply_set.count(), 1)


class TagsTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = create_sample_user()
        self.tag1 = 'tag1'
        self.tag2 = 'tag2'
        self.question1 = create_sample_question(user, tags=[self.tag1, self.tag2])
        self.question2 = create_sample_question(user, tags=[self.tag1])
    
    def test_filter_questions_with_tag(self):
        response = self.client.get(reverse('action:question-list') + '?tag=' + self.tag1)
        self.assertEqual(2, len(response.context['question_list'].all()))

        response = self.client.get(reverse('action:question-list') + '?tag=' + self.tag2)
        self.assertEqual(1, len(response.context['question_list'].all()))
