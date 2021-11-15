from django.db.models.fields import EmailField
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic.base import RedirectView, TemplateView
from users.forms import CheckoutForm, CustomChangePasswordForm, LoginForm,  RegistrationForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages

from django.views.generic import CreateView
from django.contrib.auth.views import  PasswordChangeView, PasswordResetView, PasswordResetConfirmView,  LogoutView


from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from users.tasks import send_confirmation_mail
from users.utils.tokens import account_activation_token



class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'users/email/password_reset_email.html'
    form_class = CustomPasswordResetForm
    template_name = 'users/forget_password.html'
    success_url = reverse_lazy('blogs')

    def get_success_url(self):
        messages.success(self.request, 'Password reset email has been sent to your email address. Please check your email address!')
        return super(CustomPasswordResetView, self).get_success_url()


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomChangePasswordForm
    template_name = 'users/forget_password.html'
    success_url = reverse_lazy('blogs')

    def get_success_url(self):
        messages.success(self.request, 'Password changed!')
        return super(CustomPasswordChangeView, self).get_success_url()



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/change_password.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('blogs')

    def get_success_url(self):
        messages.success(self.request, 'Password changed successfully!')
        return super(CustomPasswordResetConfirmView, self).get_success_url()



class SignupLoginView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('blogs')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blogs')
        return super(SignupLoginView, self).dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] =  RegistrationForm()
        context['login_form'] = LoginForm()
        return context
    def post(self, request, *args, **kwargs):
        login_form = LoginForm
        register_form = RegistrationForm
        if 'register' in request.POST:
            print(register_form.errors)
            register_form = RegistrationForm(data=request.POST)
            print(register_form.errors)
            if register_form.is_valid():
                register_form.instance.is_active = False
                result = super().form_valid(register_form)
                user = register_form.instance
                send_confirmation_mail(user)
                messages.success(self.request, 'You registered successfully! Check your email for verification!')
                return result
            messages.error(self.request, 'Sorry, invalid email or password. Please, double-check your credentials')
        else:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data.get('username'), 
                                    password=login_form.cleaned_data.get('password'))
                if user:
                    django_login(request, user)
                    messages.success(request, 'You are logged in!')
                    print(request.POST.get('next'))
                    if request.POST.get('next') != '':  #if user redirected to login page through some page
                        next = request.POST.get('next')
                        return HttpResponseRedirect(next)
                    return redirect('index')
                else:
                    messages.error(request, 'Sorry, invalid username or password. Please, double-check your credentials')
                    return redirect(reverse_lazy('users-login'))
            result = super().form_valid(login_form)
        return super().post(request, *args, **kwargs)



def activate(request, uidb64, token):

    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(pk=uid, is_active=False).first()
    if user is not None and account_activation_token.check_token(user, token):
        messages.success(request, 'Your account is activated!')
        user.is_active = True
        user.save()
        logout(request)
        return redirect('users-login')
    else:
        messages.error(request, 'Your link is expired or it is invalid')
        return redirect('blogs')




class MyAccountView(CreateView):
    form_class = CheckoutForm
    template_name = 'users/my-account.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'You have successfully created an account!')
        return result

    def form_invalid(self, form):
        messages.error(self.request, 'You failed to create an account! Check fields again!')
        return self.render_to_response(self.get_context_data(form=form))




def logout(request):
    django_logout(request)
    messages.success(request, 'You are logged out')
    return redirect(reverse_lazy('blogs'))




class DashBoardView(TemplateView):
    template_name = 'users/dashboard.html'
