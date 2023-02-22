from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SupportForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required  #this @ is called a decorator and adds functionality to existing function
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Your account has been successfully updated')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form':user_update_form,
        'p_form':profile_update_form
    }
    
    return render(request, 'users/profile.html', context)

class PublicProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/public_profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        profile = get_object_or_404(Profile, user=user)
        return profile
    
class SupportView(LoginRequiredMixin, FormView):
    form_class = SupportForm
    template_name = 'users/support.html'
    success_url = '/'
    
    def form_valid(self, form):
        message = form.cleaned_data['message']
        send_mail(
            'Support Request',
            message,
            self.request.user.email,
            ['max.duchesne@gmail.com'],
            fail_silently=False,
        )
        messages.success(self.request, 'Thank you for contacting us. We will get back to you as soon as we can')
        return super().form_valid(form)