from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from product.models import (Category, Discount, Review, Product, Properity, ProperityOption, 
                Image, ShoppingCart, Tag,Wishlist,Color)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'created_at', 'email', 'description')
    list_filter = ('name', 'product', 'created_at', 'email', 'description')
    search_fields = ('name', 'product', 'created_at', 'email', 'description')


admin.site.register(Review, ReviewAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'content', 'price', 'category')

    list_filter = ('category__title', 'description', 'content')

    search_fields = ('title', 'category__title',  'description')


class CategoryAdmin(TranslationAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'parent_cat', )
    list_filter = ('title', 'created_at', 'updated_at', 'parent_cat')
    search_fields = ('title', 'created_at', 'updated_at', 'parent_cat')



admin.site.register(Category, CategoryAdmin)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title','types','amount','is_active', 'created_at', 'updated_at')
    list_filter = ('title','types','amount','is_active', 'created_at', 'updated_at')
    search_fields = ('title','types','amount','is_active', 'created_at', 'updated_at')

@admin.register(Properity)
class ProperityAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'created_at', 'updated_at')


@admin.register(ProperityOption)
class ProperityOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'created_at', 'updated_at')



@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('title', 'created_at')
    search_fields = ('title', 'created_at')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list = ('product__title')
    search_fields = (['product__title'])


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (['title'])
    search_fields = (['title'])


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (['product'])

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (['product'])
 