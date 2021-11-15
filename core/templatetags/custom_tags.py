from blog.models import BlogPost
from django.template import Library
from product.models import  Category, Properity, ProperityOption
from core.forms import ContactForm



register = Library()

@register.simple_tag
def get_categories(limit=None):
    return Category.objects.filter(parent_cat=None)[0:limit]

@register.simple_tag
def forms():
    return ContactForm()

@register.simple_tag
def get_properties():
    return Properity.objects.order_by('created_at')

@register.simple_tag
def get_blogposts():
    return BlogPost.objects.order_by('created_at')
