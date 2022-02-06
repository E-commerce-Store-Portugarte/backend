from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('adminStore.api.v1.urls'))
]