from django import forms
from .models import Event, Race, Circuit, Car

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name_event', 'type', 'mode', 'document']
        widgets = {
            'type': forms.Select(choices=[('pubblico', 'Pubblico'), ('privato', 'Privato')]),
            'mode': forms.Select(choices=[('singola', 'Singola'), ('squadre', 'A Squadre'), ('torneo', 'Torneo')])
        }

class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = ['status', 'length', 'weather', 'race_start', 'qualification', 'time_progress', 
                  'dynamic_tyre', 'tyre_wear', 'dub_ghost', 'penalty', 'disqualified', 'box_stop']

class CircuitForm(forms.ModelForm):
    class Meta:
        model = Circuit
        fields = ['name', 'location', 'length']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'driver', 'performance_rating']