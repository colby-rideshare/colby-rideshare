from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Ride, RideRequest, GasPrice
from .forms import RideSignUpForm, RideCreateForm, RideUpdateForm, RideFilterForm, RideRequestForm
import os
from . import gmaps
from . import GAS_API, GOOGLE_API
from datetime import timedelta
from django.utils import timezone
import http.client
import json

def landing_page(request):
    context = {'user': request.user}
    return render(request, 'carpool/landing.html', context)

class RideListView(LoginRequiredMixin, ListView):
    model = Ride
    template_name = 'carpool/home.html'  #without this, by default, checks for 'app_name/model_name_viewtype.html (here viewtype is ListView)
    context_object_name = 'rides'  #without this, by default, calls context "object list" instead of "rides" like we do here
    ordering = ['departure_day']  #this is way to change ordering -- eventually need to change to prioritize best ride matches
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        target_date = self.request.GET.get('target_date')
        if target_date:
            queryset = queryset.filter(departure_day=target_date)
            if not queryset.exists():
                messages.warning(self.request, 'No rides found for the selected date')
        queryset = queryset.exclude(driver=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        #self.get_gas_price()
        context = super().get_context_data(**kwargs)
        context['form'] = RideFilterForm()
        for ride in context['rides']:
            ride.spots_left = ride.capacity - ride.num_riders
            ride.origin_code = ride.origin
            ride.dst_code = ride.destination
            ride.GOOGLE_API = GOOGLE_API
        return context
    

    
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
                'authorization': "apikey " + GAS_API
                }
            connection.request("GET", "/gasPrice/stateUsaPrice?state=ME", headers=headers)
            response = connection.getresponse()
            data = response.read()  #dtype is bytes
            data_string = data.decode("utf-8")  #decode to utf8
            data_dict = json.loads(data_string)  #load as dict
            if data_dict['success'] == False:
                print('API DOWN')
                return 
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
        #self.get_gas_price()
        context = super().get_context_data(**kwargs)
        context['first_name'] = context['rides'][0].driver.first_name
        context['last_name'] = context['rides'][0].driver.last_name
        for ride in context['rides']:
            ride.spots_left = ride.capacity - ride.num_riders
            ride.origin_code = ride.origin
            ride.dst_code = ride.destination
            ride.driver = ride.driver
        return context
    
class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    form_class = RideCreateForm
    # fields = ['origin','destination','departure_time','notes','capacity']
    success_url = '/'
    def form_valid(self, form):
        form.instance.driver = self.request.user
        form.instance.num_riders = 0
        response = super().form_valid(form)
        messages.success(self.request, 'Your ride has been created successfully')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_API'] = GOOGLE_API
        return context
    
class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    form_class = RideUpdateForm
    #fields = ['origin','destination','departure_time','notes','capacity']
    template_name = 'carpool/ride_update_form.html'
    success_url = '/'
    
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.driver:
            return True
        return False
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your ride has been updated successfully')
        return response
    
class RideSignUpView(LoginRequiredMixin, CreateView):
    model = RideRequest
    form_class = RideSignUpForm
    template_name = 'carpool/ride_signup_form.html'
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ride'] = Ride.objects.get(pk=self.kwargs['ride_pk'])
        context['GOOGLE_API'] = GOOGLE_API
        return context
    
    def form_valid(self, form):
        ride_request = form.save(commit=False) #commit = False saves it to memory but not DB, so can still modify before saving to DB
        ride = Ride.objects.get(pk=self.kwargs['ride_pk'])
        ride_request.ride = ride
        ride_request.passenger = self.request.user
        ride_request.save()
        
        #send email to driver
        subject = f"{self.request.user.first_name} {self.request.user.last_name} is looking for a ride"
        message = f"Message from {self.request.user.first_name}: {form.cleaned_data['message']}\n\n" \
                  f"Please visit this link to view the ride request: {self.get_ride_request_url(ride_request)}"
        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [ride.driver.email]
        send_mail(subject, message, from_email, recipient_list)
        
        #send email to passenger
        subject = f"Your ride request was successful"
        message = f"{ride.driver.first_name} has been contacted. Your ride request is pending approval."
        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [self.request.user.email]
        send_mail(subject, message, from_email, recipient_list)
        
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully contacted the driver')
        return response
    
    def get_ride_request_url(self, ride_request):
        ride_request_url = reverse('ride-request', args=[ride_request.ride.pk, ride_request.pk])
        return self.request.build_absolute_uri(ride_request_url)
    
class RideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    success_url = '/'
    
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.driver:
            return True
        return False
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.warning(self.request, 'Your ride has been deleted')
        return response
    
class RideRequestView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RideRequest
    form_class = RideRequestForm
    template_name = 'carpool/ride_request.html'
    context_object_name = 'ride_request'
    success_url = '/'
    
    def test_func(self):
        ride_request = self.get_object()
        if self.request.user == ride_request.ride.driver:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride_request = self.get_object()
        ride = ride_request.ride
        context['ride'] = ride
        context['GOOGLE_API'] = GOOGLE_API
        return context
    
    def form_valid(self, form):
        ride_request = RideRequest.objects.get(pk=self.kwargs['pk'])
        ride_request.accepted = True
        ride_request.save()
        
        #send email to driver
        subject = f"You have accepted {ride_request.passenger.first_name} {ride_request.passenger.last_name}'s carpool request"
        message = f"Thank you for helping the Colby community. " \
          f"Please be mindful of {ride_request.passenger.first_name}'s travel plans -- " \
          f"let {ride_request.passenger.first_name} know as soon as possible if anything changes."

        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [ride_request.ride.driver.email]
        send_mail(subject, message, from_email, recipient_list)
        
        #send email to passenger
        subject = f"{ride_request.ride.driver.first_name} {ride_request.ride.driver.last_name} has accepted your ride request"
        message = f"{ride_request.ride.driver.first_name} {ride_request.ride.driver.last_name} is able to drive you to {ride_request.destination}. " \
          f"Please be sure to thank your driver and to offer to chip in on gas costs -- it is more expensive than you think!"

        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [ride_request.passenger.email]
        send_mail(subject, message, from_email, recipient_list)
        
        response = super().form_valid(form)
        messages.success(self.request, 'Thank you for helping the Colby community')
        return response