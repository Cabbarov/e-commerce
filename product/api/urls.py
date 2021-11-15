from product.models import Wishlist
from django.urls import path


from product.api.views import (ProductsAPIView, ProductAPIView, CategoriesAPIView, 
                        CategoryAPIView,CartItemsAPIView, WishlistItemAPIView, WishlistItemsAPIView, CartItemAPIView)
app_name = 'products_api'

urlpatterns = [

    path('product-list/', ProductsAPIView.as_view(), name='product-list'),
    path('product-list/<int:pk>', ProductAPIView.as_view(), name='product_detail'),
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('categories/<int:pk>', CategoryAPIView.as_view(), name='category'),  
    path('cartitems/', CartItemsAPIView.as_view(), name='carts'), 
    path('cartitems/<int:pk>', CartItemAPIView.as_view(), name='cart'),
    path('wishlistitems/', WishlistItemsAPIView.as_view(), name='wishlists'),
    path('wishlistitems/<int:pk>', WishlistItemAPIView.as_view(), name='wishlist'), 
]