from django.contrib import admin
from core.models import Contact, Slider


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email')

admin.site.register(Slider)