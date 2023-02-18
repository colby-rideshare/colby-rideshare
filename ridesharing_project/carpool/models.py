from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Ride(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_day = models.DateField()
    time = models.CharField(max_length = 100)
    #departure_time = choices for different times of day
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    capacity = models.IntegerField()
    num_riders = models.IntegerField()
    
    # should create __str__ method to name rides so they aren't "ride object"
    
    def get_absolute_url(self):
        return reverse('ride-detail',kwargs={'pk':self.pk})  #gets url of specific ride detail page