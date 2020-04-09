from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Question


class QuestionListView(ListView):
    paginate_by = 30
    model = Question
