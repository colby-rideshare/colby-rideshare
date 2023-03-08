from django.db import models
from django.contrib.auth.models import User
#from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # on_delete argument deals with what to do if user is deleted
    # models.CASCADE means if user is deleted, delete their profile, but if profile is deleted, keep user
    image = models.ImageField(verbose_name='Profile picture', default='default.jpg', upload_to='profile_pics')  #user profile pic
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"
    
    # method to resize large images when saving profile images locally
    # need to figure out how to do this with AWS S3
    
    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)  #calls save method of parent models.Model class
    #     img = Image.open(self.image.path)  #opens image of current instance
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)