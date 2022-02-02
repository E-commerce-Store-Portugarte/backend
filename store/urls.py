from django.urls import path, include
from store import views

urlpatterns = [
    path('', views.home),
    path('api/v1/', include('store.api.v1.urls')),
]