from django.urls import path, include
from store import views

urlpatterns = [
    path('', views.home),
    path('login', views.home),
    path('paypal', views.home),
    path('contact', views.home),
    path('register', views.home),
    path('mercadinho', views.home),
    path('shopping-cart', views.home),
    path('products/<int:id>', views.home),
    path('api/v1/', include('store.api.v1.urls')),
]