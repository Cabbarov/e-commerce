from math import prod
from django.db.models.base import Model
from django.http import JsonResponse, Http404, request
from django.views.generic.edit import CreateView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from product.api.serializers import (CartSerializer, ProductSerializer, ProductListSerializer, WishlistSerializer,
                                     CategoryListSerializer, CategorySerializer, WishlistListSerializer, CartListSerializer)
from product.models import Product, ShoppingCart, Wishlist
from product.models import Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status


class ProductsAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductSerializer
        return super(ProductsAPIView, self).get_serializer_class()


class ProductAPIView(APIView):
    def get(self, *args, **kwargs):
        product = Product.objects.filter(pk=kwargs.get('pk')).first()
        if not product:
            raise Http404
        serializer = ProductListSerializer(
            product, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

    def put(self, *args, **kwargs):
        product = Product.objects.filter(pk=kwargs.get('pk')).first()
        if not product:
            raise Http404
        serializer = ProductSerializer(data=self.request.data,
                                       instance=product, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False)

    def delete(self, *args, **kwargs):
        product = Product.objects.filter(pk=kwargs.get('pk')).first()

        if not product:
            raise Http404
        serializer = ProductListSerializer(product)
        product.delete()
        return Response(serializer.data, safe=False)


class CategoriesAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(
            categories, many=True, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

    def post(self, *args, **kwargs):
        category_data = self.request.data
        serializer = CategorySerializer(data=category_data, context={
                                        'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False, status=201)


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, *args, **kwargs):
        category = Category.objects.filter(pk=kwargs.get('pk')).first()
        if not category:
            raise Http404
        serializer = CategoryListSerializer(
            category, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

    def delete(self, *args, **kwargs):
        category = Category.objects.filter(pk=kwargs.get('pk')).first()
        print(category)
        category.delete()
        return Response('Category is deleted', status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        category = Category.objects.filter(pk=kwargs.get('pk')).first()
        serializer = CategorySerializer(category, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemsAPIView(APIView):

    def get(self, *args, **kwargs):
        cart = ShoppingCart.objects.all()
        serializer = CartListSerializer(
            cart, many=True, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

    def post(self, *args, **kwargs):
        cart_data = self.request.data
        serializer = CartSerializer(data=cart_data, context={
            'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False, status=201)


class CartItemAPIView(APIView):

    def get(self, *args, **kwargs):
        item = ShoppingCart.objects.filter(product=kwargs.get('pk')).first()
        if not item:
            raise Http404
        serializer = CartListSerializer(
            item, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

    def delete(self, *args, **kwargs):
        item = ShoppingCart.objects.filter(product=kwargs.get('pk')).first()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, *args, **kwargs):
        item = ShoppingCart.objects.filter(product=kwargs.get('pk')).first()
        if not item:
            raise Http404
        serializer = CartSerializer(data=self.request.data,
                                    instance=item, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False)


class WishlistItemsAPIView(APIView):

    def get(self, *args, **kwargs):
        wishlist = Wishlist.objects.all()
        serializer = WishlistListSerializer(
            wishlist, many=True, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

    def post(self, *args, **kwargs):
        wishlist_data = self.request.data
        serializer = WishlistSerializer(data=wishlist_data, context={
                                        'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False, status=201)


class WishlistItemAPIView(APIView):

    def get(self, *args, **kwargs):
        item = Wishlist.objects.filter(product=kwargs.get('pk')).first()
        
        if not item:
            raise Http404
        serializer = WishlistListSerializer(
            item, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

    def delete(self, *args, **kwargs):
        item = Wishlist.objects.filter(product=kwargs.get('pk')).first()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
