from django import forms
from .models import Ride

class RideSignUpForm(forms.ModelForm):
    
    class Meta:
        model = Ride
        fields = ['num_riders']
