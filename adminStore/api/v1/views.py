from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_auth.views import LoginView
from adminStore.api.v1.serializers import ProductFormSerializer, ProductSerializer
from store.models import Product, ProductImage
from django.shortcuts import HttpResponse


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]

    def create(self, request):
        new_product = Product.objects.create(name=request.data['name'], description=request.data['description'],
                                             stock=request.data['stock'], price=request.data['price'])
        ProductImage.objects.create(image=request.data['image'], product=new_product)
        return HttpResponse(status=201)

    def get(self, request, pk):
        return Response(ProductSerializer(Product.objects.get(pk=pk)).data, status=200)


    def update(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.name = request.data['name']
        product.description = request.data['description']
        product.stock = request.data['stock']
        product.price = request.data['price']
        if request.data['image'] != '':
            product.image = request.data['image']
        product.save()
        return HttpResponse(status=200)

    def delete(self, request, pk):
        Product.objects.get(pk=pk).delete()
        return HttpResponse(status=200)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        return ProductFormSerializer


class AdminLoginView(LoginView):

    def get_response(self):
        original_response = super().get_response()
        if self.request.user.is_staff or self.request.user.is_superuser:
            aditional_data = {"is_staff": True}
            original_response.data.update(aditional_data)
            return original_response
