
from math import trunc
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from product import models
from product.models import Product, Category, ProperityOption, ShoppingCart, Tag, Properity, Wishlist,Color
from PIL import Image



class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = (
            'id',
            'title',
        )


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'parent_cat',
            'properity',
            'created_at',
            'updated_at',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'title',
            'created_at',
            'updated_at'
        )


class ProperityOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProperityOption
        fields = (
            'id',
            'title',
            'created_at',
            'updated_at',
        )


class ProductSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Product
        fields = (   
            'title',
            'description',
            'category', 
            'price',
            'discount_price',
            'tags',
            'title',
            'slug',
            'cover_image',
            'created_at',
            'updated_at',
            'properity_options',
            'color',
        )
        read_only_fields = ('author',)

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['added_by'] = request.user
        return super(ProductSerializer, self).validate(attrs)


class ProductListSerializer(ProductSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    properity_options = ProperityOptionSerializer(many=True)
    # color = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'tags',
            'category',
            'properity_options',
            'color',
            'price',
            'cover_image',
            'get_final_price'
        )



class ProperitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Properity
        fields = (
            'id',
            'title',
            'created_at',
            'updated_at',
        )





class CategoryListSerializer(CategorySerializer):
    properity = ProperitySerializer(many=True)
    parent_cat = serializers.PrimaryKeyRelatedField(read_only=True)



class  CartListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    class Meta:
        model = ShoppingCart
        fields = (
            'product',
            'quantity',
            'user',
            'color',
            'size',
        )



class  CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = (
            'product',
            'quantity',
            'user',
            'color',
            'size',
        )




class WishlistListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    class Meta:
        model = Wishlist
        fields = (
            'product',
            'user',
            'color',
            'size',
        )


class  WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = (
            'product',
            'user',
            'color',
            'size',

        )