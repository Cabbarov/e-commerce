from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.SignupLoginView.as_view(), name='users-login'),
    path('my-account/', views.MyAccountView.as_view(), name='users-my-account'),
    path('logout/', views.logout, name="logout"),
    path('confirmation/<str:uidb64>/<str:token>/', views.activate, name='confirmation'),
    path('forget-password/', views.CustomPasswordResetView.as_view(), name='password-reset-view'),
    path('reset-password/<str:uidb64>/<str:token>/',views.CustomPasswordResetConfirmView.as_view(), name='reset-password'),
    path('change-password/',views.CustomPasswordChangeView.as_view(), name='change-password'),
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
]

