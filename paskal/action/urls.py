from django.urls import path

from .views import QuestionListView, QuestionView


app_name = 'action'
urlpatterns = [
    path('questions', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>', QuestionView.as_view(), name='question-detail')
]
