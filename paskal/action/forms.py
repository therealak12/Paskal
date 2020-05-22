from django.contrib.auth.forms import forms

from .models import Question, Answer, Reply


class QuestionCreateForm(forms.ModelForm):
    title = forms.CharField(
        label='عنوان پرسش',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'dir': 'rtl',
            }
        )
    )

    text = forms.TextInput()

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')


class AnswerCreateForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'dir': 'rtl',
                'rows': 15,
                'style': 'resize: none;'
            }
        )
    )

    class Meta:
        model = Answer
        fields = ('text',)


class ReplyCreateForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'dir': 'rtl',
                'rows': 5,
                'style': 'resize: none;'
            }
        )
    )

    class Meta:
        model = Reply
        fields = ('text',)
