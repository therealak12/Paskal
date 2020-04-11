from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Question


class QuestionListView(ListView):
    paginate_by = 30
    model = Question


class QuestionView(DetailView):
    model = Question
