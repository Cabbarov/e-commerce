from django.urls import path
from product import views 

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-complete/', views.OrdercompleteView.as_view(), name='order-complete'),
    path('', views.ProductView.as_view(), name='product-list'),
    path('single-product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/', views.WishlistView.as_view(), name='product-wishlist'),
    path('filter-data/',views.filter_data,name='filter_data'),
    path('searchs/', views.searchs, name='search'),
]