from django.contrib.auth.forms import forms

from .models import Question


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
    text = forms.CharField(
        label='متن پرسش',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'dir': 'rtl',
            }
        )
    )

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')
