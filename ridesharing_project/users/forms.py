from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

#create new user creation form that inherits from default django one
#we want user to also input other fields such as email
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        
# try to make it so that profile can be created right away without needing user first
# class ProfileRegisterForm(UserCreationForm):
#     class Meta:
#         model = Profile
#         fields = ['image']
        
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
        