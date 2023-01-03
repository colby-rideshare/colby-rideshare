from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Ride(models.Model):
    origin = models.TextField()
    destination = models.TextField()
    departure_time = models.DateTimeField(default=timezone.now)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField()
    
    # should create __str__ method to name rides so they aren't "ride object"
    
    def get_absolute_url(self):
        return reverse('ride-detail',kwargs={'pk':self.pk})  #gets url of specific ride detail page