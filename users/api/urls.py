from users.api.views import SubscribeAPIView
from django.urls import path

app_name = 'users_api'

urlpatterns = [
    path('subscribe/', SubscribeAPIView.as_view(), name='subscribe'),
]