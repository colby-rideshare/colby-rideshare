from django import forms
from .models import Ride, RideRequest
from bootstrap_datepicker_plus.widgets import DatePickerInput

class RideSignUpForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['origin', 'destination', 'message']
        widgets = {
            'origin': forms.TextInput({'id': 'origin', 'type': 'text'}),
            'destination': forms.TextInput({'id': 'destination', 'type': 'text'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class RideRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['accepted']
        
class RideDeclineRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['declined']

class RideCreateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['origin','destination','departure_day','time', 'notes','capacity']
        widgets = {
            #the date time picker documentation is here: https://pypi.org/project/django-bootstrap-datepicker-plus/#description
            'departure_day': DatePickerInput(),
            'origin' : forms.TextInput({'id':'origin', 'type': 'text'}),
            'destination' : forms.TextInput({'id':'destination', 'type': 'text'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'i.e. "Will be making a stop to grab food" or "I don\'t have a set departure time and would be happy to leave earlier or later"', 'required': False}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'time': forms.Select(choices=Ride.TIME_CHOICES, attrs={'class': 'form-control', 'placeholder': ''})
        }
        
    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if not self.cleaned_data['notes']:
    #         instance.notes = "N/A"
    #     if commit:
    #         instance.save()
    #     return instance
    
class RideUpdateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['origin','destination','departure_day','time', 'notes','capacity']
        widgets = {
            #the date time picker documentation is here: https://pypi.org/project/django-bootstrap-datepicker-plus/#description
            'departure_day': DatePickerInput(),
            'origin' : forms.TextInput({'id':'origin', 'type': 'text'}),
            'destination' : forms.TextInput({'id':'destination', 'type': 'text'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ex: Need to pick up a friend at Bowdoin', 'required': False}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'time': forms.Select(choices=Ride.TIME_CHOICES, attrs={'class': 'form-control', 'placeholder': ''})
        }
        
class RideFilterForm(forms.Form):
    ANY = 'Any'
    MORNING = 'Morning'
    AFTERNOON = 'Afternoon'
    EVENING = 'Evening'
    TIME_CHOICES = (
        (ANY, 'Any'),
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon'),
        (EVENING, 'Evening'),
    )
    
    departure_date = forms.DateField(required=False, widget=DatePickerInput())
    departure_time = forms.ChoiceField(choices=TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        fields = ['departure_date', 'departure_time']
