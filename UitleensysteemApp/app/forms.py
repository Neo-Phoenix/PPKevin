# forms.py
from django import forms
from app.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['eventType', 'itemid', 'start', 'end']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
        }