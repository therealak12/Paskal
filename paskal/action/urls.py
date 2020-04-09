from django.urls import path

from .views import questions

urlpatterns = [
    path('questions', questions, name='questions'),
]