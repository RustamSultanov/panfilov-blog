from django import forms
from django.core.validators import EmailValidator

from mickroservices.models import QuestionModel


class QuestionForm(forms.ModelForm):
    # email = forms.CharField(validators=[EmailValidator])
    class Meta:
        model = QuestionModel
        exclude = ['name', 'status', 'answer', 'user']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        exclude = ['name', 'user', 'status', 'body', 'theme']
        widgets = {
            'answer': forms.Textarea(attrs={'rows': 5}),
            'hide': forms.CheckboxInput(attrs={
                    'class': "custom-control-input"})
        }
