from django import forms
from django.forms import widgets
from django.forms.fields import EmailField
from users.models import Checkout
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, UsernameField, PasswordResetForm, SetPasswordForm

User = get_user_model()


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = (
            'first_name',
            'last_name',
            'email',
            'country',
            'address',
            'city',
            'phone_number',
            'information',
            'address_title'
        )

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address'
            }),
            'country': forms.TextInput(attrs={
                'class': 'custom-select',
                'placeholder': 'Country'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'custom-select',
                'placeholder': 'Town/City'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Mobile Phone'
            }),
            'information': forms.Textarea(attrs={
                'class': 'custom-mess',
                'placeholder': 'Additional Information'
            }),
            'address_title': forms.TextInput(attrs={
                'class': 'input-text'
            })
        }


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
                'placeholder': 'Phone here...'
            }))

    class Meta:
        model = User
        fields = {
            'username',
            'email',
            'password1',
            'password2',
            'phone_number'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username here..'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email here...'
            })
        }

    def _post_clean(self):
        super()._post_clean()
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1


    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')
        if password1 != password2:
            raise forms.ValidationError('Confirm password is not same with password')
        return password2



    
class LoginForm(forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
                                                           'placeholder': 'Username'
                                                           }))

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
                'placeholder': 'Password'
            }),
    )



class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }), max_length=254)



class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        }),
    )


class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Old Password'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        }),
    )