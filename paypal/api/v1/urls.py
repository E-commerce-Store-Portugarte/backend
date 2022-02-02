from django.urls import path
from paypal.api.v1.views import create_paypal_order
from paypal.api.v1.webhook_views import paypal_webhooks

urlpatterns = [
    path('orders/', create_paypal_order),
    path('webhooks/', paypal_webhooks),

]