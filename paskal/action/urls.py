from django.urls import path

from .views import QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView
from django.contrib.auth.decorators import login_required


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
]
