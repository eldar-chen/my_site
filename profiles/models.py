from django.db import models

# Create your models here.

class UserProfile(models.Model):
    image = models.ImageField(upload_to="images") ## FileField does not upload the file to the database. 
                               ## File will be taken and moven somewhere on our harddrive and the path will be stored in the database
