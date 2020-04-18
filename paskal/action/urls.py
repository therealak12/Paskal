from django.urls import path

from .views import QuestionListView, QuestionView, QuestionCreate
from django.contrib.auth.decorators import login_required


app_name = 'action'
urlpatterns = [
    path('questions', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>', QuestionView.as_view(), name='question-detail'),
    path('questions/new', login_required(QuestionCreate.as_view()), name='question-create')
]
