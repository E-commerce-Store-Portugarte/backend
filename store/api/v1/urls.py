from django.urls import path, include
from store.api.v1 import routers
from store.api.v1.views import ProductViewSet, OrderViewSet, BasketItemViewSet

ProductRouter = routers.ProductRouter()
OrderRouter = routers.OrderRouter()
BasketItemRouter = routers.BasketItemRouter()

ProductRouter.register('products', ProductViewSet, basename='products')
OrderRouter.register('orders', OrderViewSet, basename='orders')
BasketItemRouter.register('basket-items', BasketItemViewSet, basename='basket-items')

urlpatterns = [
    path('', include(ProductRouter.urls)),
    path('', include(OrderRouter.urls)),
    path('', include(BasketItemRouter.urls)),
]