from django.conf import settings
from django.db import models
from store.models import Product
from django.contrib.auth import get_user_model
from requests import post

User = get_user_model()


class PayPalPayer(models.Model):

    user = models.ForeignKey(User, related_name='paypal_payer', on_delete=models.SET_NULL, null=True)
    given_name = models.CharField(max_length=140)
    surname = models.TextField(max_length=140, null=True, blank=True)
    email_address = models.EmailField()
    paypal_id = models.CharField(max_length=13, unique=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        verbose_name = 'PayPal Payer'
        verbose_name_plural = 'PayPal Payers'

    def __str__(self):
        return 'PayPal Payer | <User: {}>'.format(self.user.username)


class PayPalOrder(models.Model):

    STATUS_OPTIONS = [
        ('COMPLETED', 'COMPLETED'),  # When the payment is captured and the money is received
        ('APPROVED', 'APPROVED'),  # When user completes a payment
        ('CREATED', 'CREATED'),  # When user goes to payment page but does not complete payment
    ]

    INTENT_OPTIONS = [
        ('CAPTURE', 'CAPTURE'),
        ('AUTHORIZE', 'AUTHORIZE')
    ]

    order_id = models.CharField(max_length=30, unique=True)
    order_status = models.TextField(choices=STATUS_OPTIONS, default='APPROVED')
    buyer = models.ForeignKey(PayPalPayer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'PayPal Order'
        verbose_name_plural = 'PayPal Orders'

    def capture(self):
        return post(
            url="https://api.sandbox.paypal.com/v2/checkout/orders/{}/capture".format(self.order_id),
            auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
            json={ "payment_source_response": "paypal" }
        ).json()

    def __str__(self):
        return 'Order ID: {} | Status: {}'.format(self.order_id, self.order_status)


class PayPalMerchant(models.Model):

    email_address = models.EmailField()
    paypal_id = models.CharField(max_length=30, unique=True)
    brand_name = models.CharField(max_length=127)

    class Meta:
        verbose_name = 'PayPal Merchant'
        verbose_name_plural = 'PayPal Merchants'

    def __str__(self):
        return '{} | {}'.format(self.brand_name, self.email_address)


class PayPalShippingAddress(models.Model):

    address_line_1 = models.TextField(null=True, blank=True)
    address_line_2 = models.TextField(null=True, blank=True)
    admin_area_2 = models.TextField(null=True, blank=True)
    admin_area_1 = models.TextField(null=True, blank=True)
    postal_code = models.TextField(null=True, blank=True)
    country_code = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'PayPal Shipping address'
        verbose_name_plural = 'PayPal Shipping addresses'

    def __str__(self):
        return '{} / {}'.format(self.country_code, self.postal_code)


class PayPalPurchaseUnit(models.Model):

    reference_id = models.CharField(max_length=256, default='default')
    currency_code = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(PayPalOrder, related_name='purchase_units', on_delete=models.CASCADE)
    shipping = models.OneToOneField(PayPalShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    merchant = models.ForeignKey(PayPalMerchant, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'PayPal Purchase Unit'
        verbose_name_plural = 'PayPal Purchase Units'

    def __str__(self):
        return 'Order ID: {} | Price: {}€'.format(self.order.order_id, self.value)


class PayPalItem(models.Model):

    purchase_unit = models.ForeignKey(PayPalPurchaseUnit, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'PayPal Sold Item'
        verbose_name_plural = 'PayPal Sold Items'

    def __str__(self):
        return '{} x {} | {}'.format(self.product, self.quantity, self.purchase_unit.order.order_id)
