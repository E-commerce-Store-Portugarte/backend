from rest_framework import serializers
from store.models import Product, Order, OrderItem, BasketItem


class ProductSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField(read_only=True)
    abbreviated_description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'id', 'abbreviated_description', 'description', 'stock', 'price', 'image']

    def get_image(self, product):
        return product.productimage_set.all()[0].image.url
        # return [obj.image.url for obj in product.productimage_set.all()]

    def get_abbreviated_description(self, product):
        try:
            abbreviation_length = self.context["abbreviation_length"]
        except KeyError:
            abbreviation_length = 170
        return product.description[:abbreviation_length]


class BasketItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BasketItem
        fields = ['creation_date', 'product', 'name', 'amount', 'price', 'id', 'images']

    def get_name(self, basket_item):
        return basket_item.product.name

    def get_price(self, basket_item):
        return basket_item.product.price * basket_item.amount

    def get_images(self, basket_item):
        return [imageObj.image.url for imageObj in basket_item.product.productimage_set.all()]


class OrderItemSerializer(serializers.ModelSerializer):

    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'creation_date', 'amount']

    def get_product(self, order_item):
        return ProductSerializer(order_item.product).data


class OrderSerializer(serializers.ModelSerializer):

    buyer = serializers.SerializerMethodField(read_only=True)
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['buyer', 'full_name', 'email', 'phone_number', 'address_line_1', 'address_line_2', 'postcode', 'delivery_instructions', 'country', 'creation_date', 'items']

    def get_buyer(self, order):
        return order.buyer.username

    def get_items(self, order):
        return OrderItemSerializer(order.orderitem_set.all(), many=True).data