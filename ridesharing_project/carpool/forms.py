from django import forms
from .models import Ride
from bootstrap_datepicker_plus.widgets import DatePickerInput

class RideSignUpForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Ride
        fields = ['message']

class RideCreateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['origin','destination','departure_day','time', 'notes','capacity']
        widgets = {
            #the date time picker documentation is here: https://pypi.org/project/django-bootstrap-datepicker-plus/#description
            'departure_day': DatePickerInput(),
            'origin' : forms.TextInput({'id':'origin', 'type': 'text'}),
            'destination' : forms.TextInput({'id':'destination', 'type': 'text'}),
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
            'capacity': forms.NumberInput(attrs={'class': 'form-control'})
        }