from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ride

class RideListView(ListView):
    model = Ride
    template_name = 'carpool/home.html'  #without this, by default, checks for 'app_name/model_name_viewtype.html (here viewtype is ListView)
    context_object_name = 'rides'  #without this, by default, calls context "object list" instead of "rides" like we do here
    ordering = ['-departure_time']  #this is way to change ordering -- eventually need to change to prioritize best ride matches
    paginate_by = 25
    
class UserRideListView(ListView):
    model = Ride
    template_name = 'carpool/user_rides.html'  #without this, by default, checks for 'app_name/model_name_viewtype.html (here viewtype is ListView)
    context_object_name = 'rides'  #without this, by default, calls context "object list" instead of "rides" like we do here
    paginate_by = 3
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))  #either gets user's username or returns 404 error
        return Ride.objects.filter(driver=user).order_by('-departure_time')  #ordering needs to be done because query overrides it when stated as in RideListView
    
class RideDetailView(DetailView):
    model = Ride
    
class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['origin','destination','departure_time','notes','capacity']
    # can change where we redirect using "success_url = 'path'"
    
    def form_valid(self, form):
        form.instance.driver = self.request.user #set driver to current logged in user
        form.instance.num_riders = 0
        return super().form_valid(form)
    
class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['origin','destination','departure_time','notes','capacity']
    success_url = '/'
    
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.driver:
            return True
        return False
    
class RideSignUpView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['num_riders']
    template_name_suffix = '_signup_form'
    success_url = '/'
    
    def test_func(self):
        ride = self.get_object()
        if self.request.user != ride.driver:
            return True
        return False
    
# def ride_signup(request, pk):
#     ride = Ride.objects.get(pk=pk)
#     if request.method == 'POST':
#         # Increment num_riders and save the updated ride instance
#         ride.num_riders += 1
#         ride.save()
#         # Redirect the user back to the ride detail page
#         return redirect('ride-detail', pk=pk)
#     else:
#         return render(request, 'carpool/ride_signup_form.html', {'ride': ride})
    
class RideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    success_url = '/'
    
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.driver:
            return True
        return False