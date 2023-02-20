from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ride, GasPrice
from .forms import RideSignUpForm, RideCreateForm
import os
from . import gmaps
from datetime import timedelta
from django.utils import timezone
import http.client
import json

def landing_page(request):
    return render(request, 'carpool/landing.html')

class RideListView(LoginRequiredMixin, ListView):
    model = Ride
    template_name = 'carpool/home.html'  #without this, by default, checks for 'app_name/model_name_viewtype.html (here viewtype is ListView)
    context_object_name = 'rides'  #without this, by default, calls context "object list" instead of "rides" like we do here
    ordering = ['departure_day']  #this is way to change ordering -- eventually need to change to prioritize best ride matches
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        self.get_gas_price()
        context = super().get_context_data(**kwargs)
        for ride in context['rides']:
            ride.spots_left = ride.capacity - ride.num_riders
            ride.origin_code = ride.origin
            ride.dst_code = ride.destination
        return context
    
    #this code gets context for rides with capacity left
    # def get_context_data(self, **kwargs):
    #     self.get_gas_price()
    #     context = super().get_context_data(**kwargs)
    #     rides_with_spots_left = []
    #     for ride in context['rides']:
    #         ride.spots_left = ride.capacity - ride.num_riders
    #         if ride.spots_left > 0:
    #             ride.origin_code = ride.origin
    #             ride.dst_code = ride.destination
    #             rides_with_spots_left.append(ride)
    #     context['rides'] = rides_with_spots_left
    #     return context

    
    #fetch gas price if current data is over one week old
    #django does not call custom methods, so need to call it in
    #an overwritten method like get_context_data
    def get_gas_price(self):
        gas_model = GasPrice.objects.first()
        current_time = timezone.now()
        if current_time > gas_model.next_update:
            
            #make api call and get gas prices in Portland, ME
            #docs: https://collectapi.com/api/gasPrice/gas-prices-api?tab=pricing
            connection = http.client.HTTPSConnection("api.collectapi.com")
            headers = {
                'content-type': "application/json",
                'authorization': "apikey 3rsMU4US801zfhAZt9Kauk:6HSs8KPnwAOqNKhLpVGf7P"
                }
            connection.request("GET", "/gasPrice/stateUsaPrice?state=ME", headers=headers)
            response = connection.getresponse()
            data = response.read()  #dtype is bytes
            data_string = data.decode("utf-8")  #decode to utf8
            data_dict = json.loads(data_string)  #load as dict
            portland_gas_price = data_dict["result"]["cities"][2]["gasoline"]  #get gasoline price in Portland, ME
            portland_gas_price = float(portland_gas_price)
            
            #update GasPrice model
            gas_model.last_update = current_time
            gas_model.next_update = current_time + timedelta(weeks=1)
            gas_model.gas_price = portland_gas_price
            gas_model.save()
    
class UserRideListView(LoginRequiredMixin, ListView):
    model = Ride
    template_name = 'carpool/user_rides.html'  #without this, by default, checks for 'app_name/model_name_viewtype.html (here viewtype is ListView)
    context_object_name = 'rides'  #without this, by default, calls context "object list" instead of "rides" like we do here
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))  #either gets user's username or returns 404 error
        return Ride.objects.filter(driver=user).order_by('departure_day')  #ordering needs to be done because query overrides it when stated as in RideListView
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for ride in context['rides']:
            ride.spots_left = ride.capacity - ride.num_riders
        return context
    
class RideDetailView(LoginRequiredMixin, DetailView):
    model = Ride
    
    def get_object(self, queryset=None):
        ride = super().get_object(queryset)
        ride.spots_left = ride.capacity - ride.num_riders
        return ride
    
class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    form_class = RideCreateForm
    # fields = ['origin','destination','departure_time','notes','capacity']
    success_url = '/rides/'
    
    def form_valid(self, form):
        form.instance.driver = self.request.user #set driver to current logged in user
        form.instance.num_riders = 0
        return super().form_valid(form)
    
class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    form_class = RideCreateForm
    #fields = ['origin','destination','departure_time','notes','capacity']
    success_url = '/rides/'
    
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.driver:
            return True
        return False
    
class RideSignUpView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    form_class = RideSignUpForm  #when fields are specified in the form class, don't need to include them as 'fields' in view
    template_name_suffix = '_signup_form'
    success_url = '/'

    def test_func(self):
        ride = self.get_object()
        if self.request.user != ride.driver:
            if ride.capacity > ride.num_riders:
                return True
        return False
    
    def post(self, request, *args, **kwargs):
        ride = self.get_object()
        ride.num_riders += 1
        ride.save()
        #email the person who signed up
        send_mail(
            'Ride Signup Confirmation',
            'You have successfully signed up for a ride',
            # "{os.environ.get('EMAIL_USER')}",
            'max.duchesne@gmail.com',
            [self.request.user.email],
            fail_silently=False,
        )
        #email the driver
        send_mail(
            'Ride Signup Notification',
            f'{self.request.user.first_name} {self.request.user.last_name} has signed up for your ride',
            # "{os.environ.get('EMAIL_USER')}",
            'max.duchesne@gmail.com',
            [ride.driver.email],
            fail_silently=False,
        )   
        
        messages.success(request, 'An email was just sent. Please check your inbox')
        return redirect('carpool-home')
    
class RideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    success_url = '/'
    
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.driver:
            return True
        return False