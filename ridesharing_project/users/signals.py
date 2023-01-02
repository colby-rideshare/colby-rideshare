from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)  #when a user is saved, send post_save signal to create_profile function
def create_profile(sender, instance, created, **kwargs):
    if created:  #if the user was created
        Profile.objects.create(user=instance)  #create Profile object from the instance of the user that was created

@receiver(post_save, sender=User)  #when a user is saved, send post_save signal to save_profile function
def save_profile(sender, instance, **kwargs):
    instance.profile.save()