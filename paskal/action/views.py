from django.shortcuts import render


def questions(request):
    return render(request, 'action/questions.html')
