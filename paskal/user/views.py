from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import UserCreationForm, AuthenticationForm, EditProfile
from django.contrib.auth.forms import PasswordChangeForm
from .models import User


def signup(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(request, user)
        return redirect('action:question-list')
    return render(request, 'user/signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('action:question-list')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('action:question-list')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'user/signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'user/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('action:question-list')


def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'user/profile.html', {'user': user})


@login_required(login_url='/users/signin')
def user_activity(request, id):
    user = User.objects.get(id=id)
    return render(request, 'user/user-activity.html', {'user': user})


@login_required(login_url='/users/signin')
def user_edit(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            user = User.objects.get(id=request.user.id)
            return render(request, 'user/profile.html', {'user': user})
    else:
        form = EditProfile(instance=request.user)
        return render(request, 'user/user-edit.html', {'form': form})


@login_required(login_url='/users/signin')
def changepass(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            user = User.objects.get(id=request.user.id)
            return render(request, 'user/profile.html', {'user': user})
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/change-pass.html', {'form': form})
