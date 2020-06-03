from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from .models import Question, Answer, Reply
from .forms import QuestionCreateForm, AnswerCreateForm, ReplyCreateForm
from taggit.models import Tag


class QuestionListView(ListView):
    paginate_by = 30
    model = Question
    ordering = ['-created_on']

    def get(self, request, *args, **kwargs):
        tag_slug = request.GET.get('tag')
        if tag_slug:
            try:
                tag = Tag.objects.get(slug=tag_slug)
                self.queryset = Question.objects.filter(tags=tag)
            except Exception:
                raise Http404()
        return super().get(request, *args, **kwargs)


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
        form.save_m2m()
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
        obj.last_updated_on = timezone.now()
        obj.save()
        form.save_m2m()
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
    was_upvoter = question.upvoters.filter(id=request.user.id)
    was_downvoter = question.downvoters.filter(id=request.user.id)
    if was_upvoter:
        question.user.score -= 10
        request.user.upvotes.remove(question)
        question.score -= 1
    if was_downvoter:
        question.user.score += 2
        request.user.downvotes.remove(question)
        question.score += 1
    if vote == 1 and not was_upvoter:
        question.user.score += 10
        request.user.upvotes.add(question)
        question.score += vote
    elif vote == -1 and not was_downvoter:
        question.user.score -= 2
        request.user.downvotes.add(question)
        question.score += vote
    request.user.save()
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
    was_upvoter = answer.upvoters.filter(id=request.user.id)
    was_downvoter = answer.downvoters.filter(id=request.user.id)
    if was_upvoter:
        answer.user.score -= 10
        request.user.upvotes.remove(answer)
        answer.score -= 1
    if was_downvoter:
        answer.user.score += 2
        request.user.downvotes.remove(answer)
        answer.score += 1
    if vote == 1 and not was_upvoter:
        answer.user.score += 10
        request.user.upvotes.add(answer)
        answer.score += vote
    elif vote == -1 and not was_downvoter:
        answer.user.score -= 2
        request.user.downvotes.add(answer)
        answer.score += vote
    request.user.save()
    answer.user.save()
    answer.save()
    response = JsonResponse({
        'score': answer.score,
    })
    response.status_code = 200
    return response


class AnswerUpdateView(UpdateView):
    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    model = Answer
    form_class = AnswerCreateForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.last_updated_on = timezone.now()
        obj.save()
        form.save_m2m()
        return redirect(reverse('action:question-detail', kwargs={'pk': self.object.target_question.id}))


class AnswerDeleteView(DeleteView):
    model = Answer

    def get_success_url(self):
        return reverse('action:question-detail', kwargs={'pk': self.object.target_question.id})

    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)