from rest_framework import viewsets
from .models import Product, ProductMedia
from .serializers import ProductMediaSerialiser, ProductSerializer
from django.db.models import Q

from .models import ProductType, ProductAttribute, ProductTypeAttribute, ProductAttributeValue
from .serializers import ProductTypeSerializer, ProductAttributeSerializer, ProductTypeAttributeSerializer, ProductAttributeValueSerializer


class ProductsViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsMediaViewsets(viewsets.ModelViewSet):  # read only
    queryset = ProductMedia.objects.all()
    serializer_class = ProductMediaSerialiser

    def get_queryset(self):
        print(10 * "s")
        pk = self.kwargs.get("pk", None)
        res = ProductMedia.objects.filter(Q(product_id__exact=pk))
        print("res", res)
        res2 = self.queryset.filter(Q(product_id__exact=pk))
        print("res2 0", res2[0].image)
        return res

    def get_object(self):
        print(10 * "x")
        pk = self.kwargs.get("pk", None)
        res2 = self.queryset.filter(Q(product_id__exact=pk))
        print("res2 0 ", res2[0])
        return res2


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductTypeAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductTypeAttribute.objects.all()
    serializer_class = ProductTypeAttributeSerializer


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
