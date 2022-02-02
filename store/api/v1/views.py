from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from store.models import Product, Order, OrderItem, BasketItem
from store.api.v1.serializers import ProductSerializer, OrderSerializer, BasketItemSerializer

NOT_AUTHENTICATED_ERROR = Response(data={"error": "You are not authenticated"}, status=401)


class ProductViewSet(ViewSet):

    def get(self, request, *args, **kwargs):
        return Response(ProductSerializer(Product.objects.get(pk=kwargs['pk'])).data, status=200)

    def list(self, request, *args, **kwargs):
        return Response(ProductSerializer(Product.objects.all(), many=True).data, status=200)


class OrderViewSet(ViewSet):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(OrderSerializer(Order.objects.get(buyer=request.user, pk=kwargs['pk'])).data, status=200)
        return NOT_AUTHENTICATED_ERROR


    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(OrderSerializer(Order.objects.filter(buyer=request.user), many=True).data, status=200)
        return NOT_AUTHENTICATED_ERROR


class BasketItemViewSet(ViewSet):

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(BasketItemSerializer(BasketItem.objects.filter(user=request.user), many=True).data, status=200)
        return NOT_AUTHENTICATED_ERROR

    def create(self, request):
        if request.user.is_authenticated:
            product = Product.objects.get(pk=request.data['product_id'])
            obj, was_created = BasketItem.objects.get_or_create(user=request.user, product=product, defaults={"amount": request.data['amount']})
            # meaning the object is new
            if not was_created:
                obj.amount += request.data['amount']
                obj.save()
            return Response(BasketItemSerializer(BasketItem.objects.filter(user=request.user), many=True).data, status=200)
        return NOT_AUTHENTICATED_ERROR

    def delete(self, request, pk):
        basket_item = BasketItem.objects.get(pk=pk)
        if request.user.is_authenticated and basket_item.user == request.user:
            basket_item.delete()
            return Response(BasketItemSerializer(BasketItem.objects.filter(user=request.user), many=True).data, status=200)

    def put(self, request, pk):
        basket_item = BasketItem.objects.get(pk=pk)
        if request.user.is_authenticated and basket_item.user == request.user and request.data['amount'] > 0:
            basket_item.amount = request.data['amount']
            basket_item.save()
            return Response(BasketItemSerializer(BasketItem.objects.filter(user=request.user), many=True).data, status=200)
