from django.db import models
from django.db.models.fields.files import ImageField


class Contact(models.Model):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=40)
    message = models.TextField()

    #moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Slider(models.Model):
    image = models.ImageField(upload_to='slider_images/')

    #moderations
    created_at = models.DateTimeField(auto_now_add=True)