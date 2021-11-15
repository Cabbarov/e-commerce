from django.forms import ModelForm
from django.db.models import fields
from core.models import Contact
from django import forms

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'name',
            'email',
            'message',
        )

        widgets = {
            'name' : forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder' : 'Enter your Name...'
            }),
            'email' : forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder' : 'Enter your email...'
            }),
            'message' : forms.Textarea(attrs={
                                'class': 'form-control',
                                'placeholder' : 'Enter your message....'
            })
        }
