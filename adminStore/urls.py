from django.urls import path, include
from store import views

urlpatterns = [
    path('api/v1/', include('adminStore.api.v1.urls'))
]