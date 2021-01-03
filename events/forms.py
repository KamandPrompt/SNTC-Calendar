from django import forms

from .models import Event

class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.DateInput):
    input_type = 'time'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'day', 'start_time', 'end_time', 'venue','overlap')
        widgets = {'day':DateInput(),'start_time':TimeInput(),'end_time':TimeInput(),'overlap':forms.Select(choices=((True, 'Yes'), (False, 'No')))}
 