from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core import validators

#create new user creation form that inherits from default django one
#we want user to also input other fields such as email
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if "@colby.edu" not in data:
            raise forms.ValidationError("Must be a Colby email address")
        return data
    
    class Meta:
        model = User
        fields = ['username','password1','password2','first_name','last_name','email']
        
class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
class SupportForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ['message']