from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage
from django.core.validators import RegexValidator
PHONE_NUMBER_REGEX = RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'only valid phone number is required')

class Checkout(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=40)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=14, validators=[PHONE_NUMBER_REGEX]) 
    information = models.TextField()
    address_title = models.CharField(max_length=35)




class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True,)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=17, blank=True)

    # def save(self, *args, **kwargs):
    #     pil_image_obj = Image.open(self.image)
    #     new_image = resizeimage.resize_width(pil_image_obj, 80)

    #     new_image_io = BytesIO()
    #     new_image.save(new_image_io, format='JPEG')

    #     temp_name = self.image.name
    #     self.image.delete(save=False)  

    #     self.image.save(
    #         temp_name,
    #         content=ContentFile(new_image_io.getvalue()),
    #         save=False
    #     )

    #     super(CustomUser, self).save(*args, **kwargs)



class Subscribe(models.Model):
    email = models.EmailField(max_length=254, unique=True,)

    #moderation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
