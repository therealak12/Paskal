from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from .models import Question, Answer
from .forms import QuestionCreateForm, AnswerCreateForm


class QuestionListView(ListView):
    paginate_by = 30
    model = Question
    ordering = ['-created_on']


class QuestionDetailView(FormMixin, DetailView):
    model = Question
    form_class = AnswerCreateForm

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['can_delete'] = True
        return context
    
    def get_success_url(self):
        return reverse('action:question-detail', kwargs={'pk': self.object.pk})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.user = self.request.user
        answer.question = self.object
        answer.save()
        return super().form_valid(form)


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionCreateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect('action:question-list')


class QuestionUpdateView(UpdateView):
    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)
    model = Question
    form_class = QuestionCreateForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_on = timezone.now()
        obj.tags.set(form.cleaned_data['tags'])
        obj.save()
        return redirect('action:question-list')


class QuestionDeleteView(DeleteView):
    model = Question

    def get_success_url(self):
        return reverse('action:question-list')

    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


def vote_question(request, pk):
    question = Question.objects.get(pk=pk)
    vote = int(request.GET.get('vote', '0'))
    question.score += vote
    if vote == 1:
        question.user.score += 10
    elif vote == -1:
        question.user.score -= 2
    question.user.save()
    question.save()
    response = JsonResponse({
        'score': question.score,
    })
    response.status_code = 200
    return response

def vote_answer(request, pk):
    answer = Answer.objects.get(pk=pk)
    vote = int(request.GET.get('vote', '0'))
    answer.score += vote
    if vote == 1:
        answer.user.score += 10
    elif vote == -1:
        answer.user.score -= 2
    answer.user.save()
    answer.save()
    response = JsonResponse({
        'score': answer.score,
    })
    response.status_code = 200
    return response
