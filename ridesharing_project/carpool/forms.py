from django import forms
from .models import Ride
from bootstrap_datepicker_plus.widgets import DatePickerInput

class RideSignUpForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['num_riders']

class RideCreateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['origin','destination','departure_day','notes','capacity']
        widgets = {
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Waterville, ME'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Boston, MA'}),
            #the date time picker documentation is here: https://pypi.org/project/django-bootstrap-datepicker-plus/#description
            'departure_day': DatePickerInput(),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ex: Need to pick up a friend at Bowdoin', 'required': False}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'})
        }
        
    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if not self.cleaned_data['notes']:
    #         instance.notes = "N/A"
    #     if commit:
    #         instance.save()
    #     return instance