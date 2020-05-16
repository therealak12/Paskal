from django.urls import path

from .views import QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView
from .views import vote_question, vote_answer
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


app_name = 'action'
urlpatterns = [
    path('questions', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/new', login_required(QuestionCreateView.as_view()),
         name='question-create'),
    path('questions/delete/<int:pk>',
         login_required(QuestionDeleteView.as_view()), name='question-delete'),
    path('questions/edit/<int:pk>',
         login_required(QuestionUpdateView.as_view()), name='question-edit'),
    path('ajax/vote_question/<int:pk>', login_required(vote_question), name='question-vote'),
    path('ajax/vote_answer/<int:pk>', login_required(vote_answer), name='answer-vote'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
