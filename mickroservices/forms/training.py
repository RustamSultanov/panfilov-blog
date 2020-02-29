from django import forms


from mickroservices.models import ScheduleModel


class ScheduleForm(forms.ModelForm):
    date_schedule = forms.DateField(
        localize=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'placeholder': "Даты занятий",
            'wtype': 'date',
            'type': 'text'
        })
    )

    class Meta:
        model = ScheduleModel
        fields = ('date_schedule', 'url_lesson')
