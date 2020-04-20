from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.utils import timezone

from .models import Question
from .forms import QuestionCreateForm


class QuestionListView(ListView):
    paginate_by = 30
    model = Question
    ordering = ['-created_on']


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['can_delete'] = True
        return context


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
