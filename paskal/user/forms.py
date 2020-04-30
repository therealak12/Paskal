from django.contrib.auth.forms import forms, ReadOnlyPasswordHashField, UserCreationForm as BaseUserCreationForm, \
    UserChangeForm as BaseUserChangeForm, PasswordChangeForm as BasePasswordChangeForm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserChangeForm

from .models import User


class UserCreationForm(BaseUserCreationForm):
    password1 = forms.CharField(
        label='گذرواژه',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='تکرار گذرواژه',
        widget=forms.PasswordInput
    )

    name = forms.CharField(label='نام کامل', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'dir': 'rtl',
        }
    ))

    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
        }
    ))

    class Meta:
        model = get_user_model()
        fields = ('email', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """ Save the user in the database"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(BaseUserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'bio', 'avatar', 'password')

    def clean_password(self):
        return self.initial["password"]


class AuthenticationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='گذر‌واژه')
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


class EditProfile(UserChangeForm):
    name = forms.CharField(label='تغییر نام', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'dir': 'rtl',
        }
    ))

    email = forms.EmailField(label='تغییر ایمیل', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
        }
    ))

    bio = forms.CharField(label='تغییر بیو', widget=forms.Textarea(
        attrs={
            'rows': 1, 'cols': 15,
            'autofocus': 'autofocus',
            'class': 'form-control',
            'dir': 'rtl',
        }
    ))

    avatar = forms.ImageField(label='تغییر عکس')

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'bio', 'avatar', 'password')
