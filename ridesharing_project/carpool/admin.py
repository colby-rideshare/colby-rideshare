from django.contrib import admin
from .models import Ride, RideRequest, GasPrice

admin.site.register(Ride)
admin.site.register(RideRequest)
admin.site.register(GasPrice)
