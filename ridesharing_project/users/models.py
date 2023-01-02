from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # on _delete argument deals with what to do if user is deleted
    # models.CASCADE means if user is deleted, delete their profile, but if profile is deleted, keep user
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  #user profile pic
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self):
        super().save()  #calls save method of parent models.Model class
        img = Image.open(self.image.path)  #opens image of current instance
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)