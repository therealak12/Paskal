from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib import messages

from .models import Question
from .forms import QuestionCreateForm


class QuestionListView(ListView):
    paginate_by = 30
    model = Question
    ordering = ['created_on']


class QuestionView(DetailView):
    model = Question


class QuestionCreate(CreateView):
    model = Question
    form_class = QuestionCreateForm
    # message = 'پرسش شما ثبت شد. ما از طریق ایمیل هر رخدادی درباره این پرسش را به شما خبر می‌دهیم!'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # messages.success(self.request, self.message)
        return reverse('action:question-list')

# commented lines can be uncommented to enable messaging, also you need to make an appropriate view in the html file too 
