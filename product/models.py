from sellshop_project.settings import Settings
import product
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import BLANK_CHOICE_DASH, CharField, IntegerField, SlugField
from django.db.models.fields.files import ImageField
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, OuterRef, Subquery
import math
from math import *


User = get_user_model()
    
class Color(models.Model):
    title = models.CharField(max_length=7, default='#FFBF00')
    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=20)
    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Properity(models.Model):
    title = models.CharField(max_length=50)
    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Properities'

    def __str__(self):
        return self.title


class Category(models.Model):
    parent_cat = models.ForeignKey('self', on_delete=models.CASCADE,
                db_index=True, related_name='parent_category', null=True, blank=True,verbose_name=_("parent_category"))
    properity = models.ManyToManyField(
        Properity, db_index=True, related_name='categories', blank=True)
    title = models.CharField(verbose_name=_('Main Category'), max_length=35)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        if self.parent_cat:
            return f'{self.parent_cat} > {self.title}'
        return self.title


class ProperityOption(models.Model):
    # relation
    properity = models.ForeignKey(Properity, on_delete=models.CASCADE,
                                  db_index=True, related_name='options')
    title = models.CharField('Option field', max_length=50, null=True, blank=True)
    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  f'{self.properity.title} > {self.title}'


class Discount(models.Model):
    Type_of_discount = [
        (1, '%'),
        (2, 'numeral'),
    ]
    title = models.CharField(max_length=100,null=True,blank=True)
    types = models.IntegerField(choices=Type_of_discount)
    is_active = models.BooleanField(default=True)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): 
        return self.title


class Product(models.Model):
    # relations
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                db_index=True, related_name='products',verbose_name="Category")

    properity_options = models.ManyToManyField(ProperityOption,
                                db_index=True, blank=True, related_name='products')
    
    tags = models.ManyToManyField(Tag,db_index=True, blank=True, related_name='products')
   
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                db_index=True, related_name='added_products', blank=True, null=True)


    discount_price = models.ForeignKey(Discount,on_delete=models.SET_NULL,
                                            db_index=True,related_name="products",null=True,blank=True)
    color = models.ManyToManyField(
        Color, db_index=True, related_name='products', blank=True)
    
    slug = models.CharField(verbose_name='Slug',max_length=140,null=True, blank=True)
    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=120)
    content = models.TextField()
    in_stock = models.BooleanField(default=True)    
    cover_image = models.ImageField(upload_to='product_cover_images/')
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    more_info = models.CharField(max_length=180, blank=True)
    # moderation
    is_published = models.BooleanField('Should it get published?', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    def get_final_price(self):
        if self.discount_price:
            if self.discount_price.types == 1 :
                return self.price - (self.price / 100 * self.discount_price.amount)
            else :
                return self.price - self.discount_price.amount  
        return self.price

    def get_sale_percent(self):
        if self.discount_price.types == 1 : 
            return self.discount_price.amount
        else:
            y = (self.discount_price.amount * 100) / self.price
            return math.floor(y)

    def avarage_rating(self):
        b = list(self.reviews.values_list('rate', flat=True))
        c = sum(b)/len(b)
        return c


    def get_absolute_url(self):
        return reverse_lazy('product_detail', kwargs={
            'slug': self.slug
        })

    

class Review(models.Model):
    """
        This model shows reviews for specific clothing
    """
    # relations
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                db_index=True, related_name='reviews')

    name = models.CharField('Your name', max_length=50)
    email = models.EmailField(max_length=100)
    description = models.TextField(max_length=500)
    rate = models.IntegerField(default=0)

    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    # relation
    product = models.ForeignKey(
        Product, on_delete=CASCADE, db_index=True, related_name="small_images")

    small_image = models.ImageField(
        upload_to='product_images/', null=True, blank=True)



class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                db_index=True, related_name='shopping_cart', blank=True, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,
                                db_index=True, related_name='in_cart', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=10, blank=True, null=True)
    size = models.CharField(max_length=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title





class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                db_index=True, related_name='wishlist', blank=True, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,
                                db_index=True, related_name='in_wishlist', blank=True, null=True)

    color = models.CharField(max_length=10, blank=True, null=True)
    size = models.CharField(max_length=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title



class BillingAddress(models.Model):

    Country_choices = [
    ('tr', 'Turkey'),
    ('az', 'Azerbaijan'),
    ('ru', 'Russia')
]
    name = models.CharField(max_length=35)
    email = models.EmailField(max_length=40)
    phone = models.IntegerField(blank=True)
    country = models.CharField(max_length=40,choices=Country_choices)
    company_name = models.CharField(max_length=40)   

    
 