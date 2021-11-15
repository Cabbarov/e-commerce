
from product.models import Product
from core.models import Slider
from blog.models import BlogPost
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.views.generic.list import ListView

from core.forms import ContactForm
from django.contrib import messages


class ErrorView(TemplateView):
    template_name = 'core/error-404.html'


class IndexView(ListView):
    template_name = 'core/index.html'
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'blogpost_list': BlogPost.objects.order_by('-created_at')[:3],
            'product_list': Product.objects.order_by('-created_at')[:4],
            'popular_product_list': Product.objects.order_by('-reviews')[:4],
            'slider_list': Slider.objects.order_by('-created_at')[:2],
        })
        return context
   
    




class ContactView(CreateView):
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = '/'

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'Thank you for request! We will get in touch with you soon!')
        return result



class AboutView(TemplateView):
    template_name = 'core/about.html'