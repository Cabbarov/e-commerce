from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.http import request
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sellshop_project.settings import SITE_ADDRESS,EMAIL_HOST_USER
from django.shortcuts import render
from django.db.models import Count
from users.utils.tokens import account_activation_token
from product.models import Product, Review
from datetime import datetime, timedelta
import time
from celery import shared_task
from users.models import Subscribe
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


def send_confirmation_mail(user):
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    redirect_url = f"http://localhost:8000{reverse_lazy('confirmation', kwargs={'uidb64': uid,'token': token})}"
    body = render_to_string('users/email/confirmation_email.html', context={
        'user': user,
        'redirect_url': redirect_url,
    })
    msg = EmailMessage(subject='Email Verification', body=body,
                       from_email=settings.EMAIL_HOST_USER, to=[user.email], )
    msg.content_subtype = 'html'
    msg.send()


@shared_task
def send_mail_to_subscribers():
    subscribers = Subscribe.objects.all().values_list('email', flat=True)

    last_week = datetime.today() - timedelta(days=7)

    products = Product.objects.filter(created_at__gte=last_week).annotate(num_reviews=Count('reviews')).order_by('-num_reviews')[:3]
    
    body = render_to_string('users/email/email-subscribers.html', context={
        'products': products,
        'SITE_ADDRESS': SITE_ADDRESS
    })
    msg = EmailMessage(subject='Product Updates', body=body,
                       from_email=EMAIL_HOST_USER, to=subscribers, )
    msg.content_subtype = 'html'
    msg.send()
    return render(request, 'users/email/email-subscribers.html' )



@shared_task
def send_mail_to_subscribers2():
    subscribers = User.objects.distinct('email').values_list('email', flat=True)
    month = datetime.today()- timedelta(minutes=1)
    users = User.objects.filter(last_login__gte=month).values_list('email', flat=True)
    products = Product.objects.all().annotate(reviews_count = Count('reviews')).order_by('-reviews_count')[:5]

    body = render_to_string('product/email-subscribers.html', context={
        'users': users,
        'products': products,
        'SITE_ADDRESS': settings.SITE_ADDRESS
    })
    msg = EmailMessage(subject='Stories News', body=body,
                    from_email=settings.EMAIL_HOST_USER, to=subscribers, )
    msg.content_subtype = 'html'
    msg.send()
