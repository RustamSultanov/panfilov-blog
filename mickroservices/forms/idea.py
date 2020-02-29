from django import forms

from mickroservices.models import IdeaModel


class IdeaForm(forms.ModelForm):
    # email = forms.CharField(validators=[EmailValidator])
    class Meta:
        model = IdeaModel
        exclude = ['status', 'answer', 'date_answer', 'date_created', ]
        widgets = {
            'body': forms.Textarea(attrs={'rows': 2}),
        }


class IdeaStatusForm(forms.ModelForm):
    class Meta:
        model = IdeaModel
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'btn btn-warning btn-xs btn-round dropdown-toggle'})
        }