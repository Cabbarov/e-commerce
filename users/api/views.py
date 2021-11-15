from users.models import Subscribe
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from django.template import context
from rest_framework.views import APIView
from blog.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import permissions, serializers
from users.tasks import send_confirmation_mail

from users.api.serializers import SubscribeSerializer, UserDetailSerializer, RegisterSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = UserDetailSerializer(user)
        return Response(user_serializer.data, status=200)


class CreateUserView(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = RegisterSerializer
    def post(self, *args, **kwargs):
        register_data = self.request.data
        serializer = RegisterSerializer(data=register_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.filter(username=serializer.validated_data['username']).first()
        send_confirmation_mail(user)
        return JsonResponse(data=serializer.data, safe=False, status=201)



class SubscribeAPIView(CreateAPIView):
    serializer_class = SubscribeSerializer
    model = Subscribe


