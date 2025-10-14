from django import forms
from .models import Event, Car, Member


class EventCreateForm(forms.ModelForm):
    """Form for creating new carpool events."""
    
    class Meta:
        model = Event
        fields = ['name', 'date', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Event name'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event location (optional)'}),
        }


class CarCreateForm(forms.ModelForm):
    """Form for adding cars to an event."""
    
    class Meta:
        model = Car
        fields = ['driver_name', 'car_name', 'capacity', 'notes']
        widgets = {
            'driver_name': forms.TextInput(attrs={'placeholder': "Driver's name"}),
            'car_name': forms.TextInput(attrs={'placeholder': 'Car name/label (optional)'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'Number of seats', 'min': 1}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional notes (optional)'}),
        }


class MemberCreateForm(forms.ModelForm):
    """Form for adding members to an event."""
    
    class Meta:
        model = Member
        fields = ['name', 'contact', 'car']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Contact info (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
        if event:
            # Only show cars from the current event
            self.fields['car'].queryset = Car.objects.filter(event=event)
            self.fields['car'].empty_label = "Unassigned (no car yet)"


class MemberUpdateForm(forms.ModelForm):
    """Form for updating member car assignment."""
    
    class Meta:
        model = Member
        fields = ['car']
    
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
        if event:
            # Only show cars from the current event
            self.fields['car'].queryset = Car.objects.filter(event=event)
            self.fields['car'].empty_label = "Unassigned (no car yet)"