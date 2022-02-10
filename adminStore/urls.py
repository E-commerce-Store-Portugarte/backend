from django.urls import path, include
from .views import dashboard

urlpatterns = [
    path('api/v1/', include('adminStore.api.v1.urls')),
    path('dashboard', dashboard),
    path('settings', dashboard),
    path('tables', dashboard),
    path('maps', dashboard),
]