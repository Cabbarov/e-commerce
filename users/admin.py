from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from users.models import Checkout,CustomUser, Subscribe



@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'country')
    list_filter = ('email', 'country', 'city')
    search_fields = ( 'email', 'country', 'city')
    
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','email')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    display = ('email')



