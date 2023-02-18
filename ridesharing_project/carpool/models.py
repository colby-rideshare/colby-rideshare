from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            ('You must have at least one spot in your car to post a ride')
        )

class Ride(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_day = models.DateField()
    #departure_time = choices for different times of day
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    num_riders = models.IntegerField()

    
    # should create __str__ method to name rides so they aren't "ride object"
    
    def get_absolute_url(self):
        return reverse('ride-detail',kwargs={'pk':self.pk})  #gets url of specific ride detail page