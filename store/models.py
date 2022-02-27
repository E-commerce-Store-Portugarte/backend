import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_product_ref():
    return uuid.uuid4()


class Product(models.Model):

    name = models.CharField(max_length=1000)
    reference = models.UUIDField(default=generate_product_ref, unique=True)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=10)

    def __str__(self):
        return '{} {}€'.format(self.name, self.price)


class ProductImage(models.Model):

    image = models.ImageField(upload_to='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.image.url


class Order(models.Model):

    paypal_order = models.OneToOneField('paypal.PayPalOrder', related_name='order',  on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    full_name = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    city = models.TextField(null=True)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(blank=True, null=True)
    postcode = models.TextField()
    delivery_instructions = models.TextField(blank=True, null=True)
    country = models.TextField(default='Portugal')
    creation_date = models.DateTimeField(auto_now_add=True)


class PrePaymentOrder(models.Model):
    """
    This Object is created when user gets redirected to PayPal payment page but haven't completed the payment yet
    This Object is used to store user's inputted data before payment is completed.
    (user inputted data needs to be stored beforehand since we can't send them all via Paypal Webhooks)
    """

    paypal_order = models.OneToOneField('paypal.PayPalOrder', on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    full_name = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    city = models.TextField(null=True)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(blank=True, null=True)
    postcode = models.TextField()
    delivery_instructions = models.TextField(blank=True, null=True)
    country = models.TextField(default='Portugal')
    creation_date = models.DateTimeField(auto_now_add=True)

    def get(self):
        return "https://api.sandbox.paypal.com/v2/checkout/orders/" + self.paypal_order.order_id

    def approve(self):
        return "https://www.sandbox.paypal.com/checkoutnow?token=" + self.paypal_order.order_id


class OrderItem(models.Model):

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveSmallIntegerField()


class BasketItem(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    def price(self):
        return float(self.product.price * self.amount)


class SupportTicket(models.Model):

    name = models.CharField(max_length=128, blank=False, null=False)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
