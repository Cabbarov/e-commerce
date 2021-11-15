from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.views.generic.base import TemplateView
import product
from django.contrib.admin import options
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.db.models import Q,Min,Max
from django.db.models import Q
from product.models import BillingAddress, Category, Image,  Product, Properity, ProperityOption, Review, ShoppingCart,Wishlist,Color
from blog.models import *
from product.forms import ReviewForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.http import JsonResponse, request
import logging
from django.core.paginator import Paginator
from .forms import CheckoutForm

logger = logging.getLogger(__name__)


from taggit.models import Tag
from django.views.generic import CreateView,ListView,DetailView



def filter_data(request):
    
    size = request.GET.getlist('Size[]')
    brand = request.GET.getlist('Brand[]')
    color = request.GET.getlist('Color[]')
    category = request.GET.getlist('Category[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allproducts = Product.objects.all().order_by('-id')
    allproducts=allproducts.filter(price__gte=minPrice)
    allproducts=allproducts.filter(price__lte=maxPrice)
    if len(size)>0:
    	allproducts=allproducts.filter(properity_options__in=size).distinct()
    if len(brand)>0:
        allproducts=allproducts.filter(properity_options__in=brand).distinct()
    if len(color)>0:
        allproducts=allproducts.filter(color__in=color).distinct()
    if len(category)>0:
        allproducts=allproducts.filter(category__in=category).distinct()
    t = render_to_string('product/products.html',{'data':allproducts})
    return JsonResponse({'data':t})



class CheckoutView(View):
    def get(self, *args,**kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'product/checkout.html',context) 
    
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = ShoppingCart.objects.get(user = self.request.user,ordered=False)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                company_name = form.cleaned_data.get('company_name')
                country = form.cleaned_data.get('country')
                address = form.cleaned_data.get('address')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    name = name,
                    email = email,
                    phone = phone,
                    country = country,
                    company_name = company_name,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                print(form.cleaned_data)
            messages.warning(self.request,'Failed checkout')
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request,'You do not have an active order')
            return redirect('checkout')


class ProductView(ListView):
    model = Product
    paginate_by=4
    template_name = 'product/product-list.html'
    def get_context_data(self, **kwargs):
        minMaxPrice = self.model.objects.aggregate(Min('price'),Max('price'))
        context = super(ProductView, self).get_context_data(**kwargs)
        category_colors = Color.objects.all()
        minMaxPrice['price__min']=int(minMaxPrice['price__min'])
        minMaxPrice['price__max']=int(minMaxPrice['price__max'])
        context["category_colors"] = category_colors
        context['minMaxPrice'] = minMaxPrice
        return context


class ProductDetailView(FormMixin, DetailView):
    model = Product
    form_class = ReviewForm
    template_name = 'product/single-product.html'

    def get_success_url(self):
        messages.success(self.request, 'Thank you for commenting!')
        return reverse("product_detail", kwargs={"slug": self.object.slug})


    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["form"] = self.get_form()
        product = Product.objects.filter(id=self.object.pk).first()
        product_category = product.category  # get product's category
        related_category = Category.objects.all().filter(title=product_category).first()
        related_products = Product.objects.all().filter(Q(category=related_category) & (~Q(id=product.id)))
        category_properities = product_category.properity.all()
        context["related_products"] = related_products
        context["category_properities"] = category_properities
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.product = self.get_object()
        form.save()
        return super().form_valid(form)

    



class WishlistView(ListView):
    model = Wishlist
    template_name = 'product/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)
        wishlist_items = Wishlist.objects.filter(user=self.request.user)

        for product in wishlist_items:
            if product:
                colors = product.product.color.all()
                for c in colors:
                    color_title = c.title
            context["color_title"] = color_title

        for product in wishlist_items:
            if product:
                options = product.product.properity_options.all()
                for option in options:
                    product_option = option.title
            context["product_option"] = product_option
        context["wishlist_items"] = wishlist_items
        return context


class CartView(TemplateView):
    template_name='product/cart.html'


class CheckoutView(TemplateView):
    template_name='product/checkout.html'


def searchs(request):
    searchs = request.GET['search']
    blogpost_list = BlogPost.objects.filter(title__icontains=searchs).order_by('-id')
    data=Product.objects.filter(title__icontains=searchs).order_by('-id')
    return render(request,'search.html',{'product_list': data,'blogpost_list':blogpost_list})


class OrdercompleteView(TemplateView):
    template_name='product/order-complete.html'
