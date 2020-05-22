from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from .models import Question, Answer, Reply
from .forms import QuestionCreateForm, AnswerCreateForm, ReplyCreateForm


class QuestionListView(ListView):
    paginate_by = 30
    model = Question
    ordering = ['-created_on']


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'action/question_detail.html'

    def get_object(self, queryset=None):
        try:
            obj = Question.objects.get(pk=self.kwargs['pk'])
        except Question.DoesNotExist:
            raise Http404('سوالی با این شماره وجود ندارد!')
        return obj

    def get_context_data(self, **kwargs):
        kwargs['question'] = self.get_object()
        if 'answer_form' not in kwargs:
            kwargs['answer_form'] = AnswerCreateForm
        if 'reply_form' not in kwargs:
            kwargs['reply_form'] = AnswerCreateForm
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = {}
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        if 'answer' in request.POST:
            answer_form = AnswerCreateForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(commit=False)
                answer.user = self.request.user
                answer.target_question = self.get_object()
                answer.save()
            else:
                context['answer_form'] = answer_form
        elif 'reply' in request.POST:
            reply_form = ReplyCreateForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.user = self.request.user
                reply.action = self.get_object()
                if 'parent_reply_id' in request.POST:
                    reply.parent = Reply.objects.get(
                        id=request.POST['parent_reply_id'])
                reply.save()
            else:
                context['reply_form'] = reply_form
        return render(request, self.template_name, self.get_context_data(**context))


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
