from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

# don't need this anymore but there is issue with exisiting db data when deleting
def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            ('You must have at least one spot in your car to post a ride')
        )
    
class Ride(models.Model):
    MORNING = 'Morning'
    AFTERNOON = 'Afternoon'
    EVENING = 'Evening'
    TIME_CHOICES = (
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon'),
        (EVENING, 'Evening'),
    )

    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_day = models.DateField()
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    num_riders = models.IntegerField()
    
    #TODO add ride passengers and ride stops
    
    def get_absolute_url(self):
        return reverse('ride-detail',kwargs={'pk':self.pk})  #gets url of specific ride detail page
    
class RideRequest(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.SET_NULL, null=True)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    message = models.TextField()
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    
#the purpose of this is to essentially serve as a timer
#current_time is updated every time a user visits the rides page
#fetch_gas_price is set to one week after the last time we fetched gas prices
#every time we fetch gas price, we reset fetch_gas_price
class GasPrice(models.Model):
    last_update = models.DateTimeField()
    next_update = models.DateTimeField()
    gas_price = models.FloatField()