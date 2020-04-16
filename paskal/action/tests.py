from django.urls import reverse
from django.test import TestCase, Client
from .models import Tag

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