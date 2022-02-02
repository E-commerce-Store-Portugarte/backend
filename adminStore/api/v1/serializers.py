from rest_framework import serializers
from store.models import Product


class ProductFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=1000, required=True)
    description = serializers.CharField(required=True)
    stock = serializers.IntegerField(required=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, required=True)
    image = serializers.ImageField(required=True)


class ProductSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'stock', 'price', 'images']

    def get_images(self, product):
        return [product.image.url for product in product.productimage_set.all()]