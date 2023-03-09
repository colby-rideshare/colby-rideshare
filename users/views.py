from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SupportForm, ProfileRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
import os


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            try:
                profile = Profile.objects.get(user=user)
                p_form = ProfileRegisterForm(request.POST, request.FILES, instance=profile)
            except Profile.DoesNotExist:
                profile = p_form.save(commit=False)
                profile.user = user
                p_form.save()
                
            #send welcome email to user
            subject = "Welcome to Colby Rideshare!"
            message = f"Hi {user.first_name},\n\nThank you for signing up for Colby Rideshare! We're excited to have you as a part of our community. " \
                f"Colby Rideshare was created for Colby students, by Colby students, to help members of our community travel to and from campus seamlessly. " \
                f"Whether you're looking for a ride to Portland Jetport or just looking for people to keep you company on a long drive back to New York, " \
                f"we hope that Colby Rideshare will bring us closer as a community and ease some of the stress that many students have when making travel plans. " \
                f"Colby Rideshare is completely free to use, although riders are encouraged to chip in for drivers' gas costs.\n\n" \
                f"To get started, simply log in at https://www.colbyrideshare.live with your username and password. From there, you can post an upcoming ride if you are driving or search for other ride offers. " \
                f"Please don't hesitate to reach out to our support team at https://www.colbyrideshare.live/support/ if you have any questions, issues, or suggestions on how we can improve. " \
                f"Thanks again for using Colby Rideshare -- please help other students find rides by encouraging fellow Mules to join!" \
                f"\n\nBest,\nThe Colby Rideshare Team"
            from_email = os.environ.get('EMAIL_USER')
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list) 
            
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    return render(request, 'users/register.html', {'u_form':u_form, 'p_form':p_form})

@login_required  #this @ is called a decorator and adds functionality to existing function
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Your account has been successfully updated')
            return redirect('landing-page')
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
            [os.environ.get('EMAIL_USER')],
            fail_silently=False,
        )
        messages.success(self.request, 'Thank you for contacting us. We will get back to you as soon as we can')
        return super().form_valid(form)