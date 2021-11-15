from django import forms
from django.forms import ModelForm
from django.forms.fields import CharField
from django.forms.widgets import TextInput, Textarea
from product.models import Color
from product.models import Review
from django import forms


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = (
            'name',
            'email',
            'description',
            'rate'
        )

        widgets = {
            'name' : forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder' : 'Your Name'
            }),
            'email' : forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder' : 'Your Email'
            }),
            'description' : forms.Textarea(attrs={
                                'class': 'form-control',
                                'placeholder' : 'Your Review'
            }),
            'rate' : forms.HiddenInput(attrs={
                'value' : ''
                
            })
        }


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = "__all__"

        widgets = {
            "name": TextInput(attrs={"type": "color"}),
        }


PAYMENT_CHOICES = {
    ('S', 'Stripe'),
    ('P', 'Paypal')
}
Country_choices = {
    ('tr', 'Turkey'),
    ('az', 'Azerbaijan'),
    ('ru', 'Russia')
}

class CheckoutForm(forms.Form):
    name = forms.CharField(widget=TextInput(attrs={'placeholder':'Your name'}))
    email = forms.EmailField(widget=TextInput(attrs={'placeholder':'Enter your email here'}))
    phone = forms.IntegerField(required=False,widget=TextInput(attrs={'placeholder':'Phone here'}))
    company_name = forms.CharField(required=False,widget=TextInput(attrs={'placeholder':'Company name here'}))
    country = forms.ChoiceField(choices=Country_choices)
    address = forms.CharField(widget=Textarea(attrs={'placeholder':'Company name here','rows':3}))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)