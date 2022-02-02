from django.urls import path, include
from . import routers
from .views import ProductViewSet, AdminLoginView

ProductRouter = routers.ProductRouter()

ProductRouter.register(prefix='products', viewset=ProductViewSet, basename='products')

urlpatterns = [
    path('', include(ProductRouter.urls)),
    path('login/', AdminLoginView.as_view())
]