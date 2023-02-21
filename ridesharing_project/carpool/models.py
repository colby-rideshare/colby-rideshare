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
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_day = models.DateField()
    time = models.CharField(max_length = 100)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    num_riders = models.IntegerField()
    #add float field for estimated gas costs (miles / mpg * current gas prices)

    
    # should create __str__ method to name rides so they aren't "ride object"
    
    def get_absolute_url(self):
        return reverse('ride-detail',kwargs={'pk':self.pk})  #gets url of specific ride detail page
    
#the purpose of this is to essentially serve as a timer
#current_time is updated every time a user visits the rides page
#fetch_gas_price is set to one week after the last time we fetched gas prices
#every time we fetch gas price, we reset fetch_gas_price
class GasPrice(models.Model):
    last_update = models.DateTimeField()
    next_update = models.DateTimeField()
    gas_price = models.FloatField()