"""sellshop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include   
from django.conf import settings
from django.conf.urls.static import static 
from django.conf.urls.i18n import i18n_patterns
from users.api.views import CustomAuthToken, CreateUserView

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  
    path('i18n/', include('django.conf.urls.i18n')),     
    path('admin/', admin.site.urls),
    path('api/', include('product.api.urls', namespace='products_api')),
    path('api/', include('users.api.urls', namespace='users_api')),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api-token-auth/register', CreateUserView.as_view()),
    path('social-auth/', include('social_django.urls', namespace="social")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path('blogs/', include('blog.urls')),
    path('products/', include('product.urls')),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
)
