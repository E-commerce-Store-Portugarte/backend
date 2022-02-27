from django.urls import path, include
from store.api.v1 import routers
from store.api.v1.views import ProductViewSet, OrderViewSet, BasketItemViewSet, SupportTicketViewSet

ProductRouter = routers.ProductRouter()
OrderRouter = routers.OrderRouter()
BasketItemRouter = routers.BasketItemRouter()
SupportTicketRouter = routers.SupportTicketRouter()

ProductRouter.register('products', ProductViewSet, basename='products')
OrderRouter.register('orders', OrderViewSet, basename='orders')
BasketItemRouter.register('basket-items', BasketItemViewSet, basename='basket-items')
SupportTicketRouter.register('support-tickets', SupportTicketViewSet, basename='support-tickets')

urlpatterns = [
    path('', include(ProductRouter.urls)),
    path('', include(OrderRouter.urls)),
    path('', include(BasketItemRouter.urls)),
    path('', include(SupportTicketRouter.urls))
]