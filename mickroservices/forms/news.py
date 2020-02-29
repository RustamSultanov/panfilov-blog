from django import forms

from mickroservices.models import NewsPage


class NewsForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.HiddenInput())
    content = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = NewsPage
        fields = ('title', 'first_published_at', 'image', 'body', 'content', 'announcement')
        widgets = {'first_published_at': forms.TextInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'placeholder': "Даты занятий",
            'wtype': 'date',
            'type': 'text'})
        }
