from rest_framework import viewsets
from .models import Product, ProductAttributeValue, ProductMedia
from .serializers import ProductAttributeValueSerializer, ProductMediaSerialiser, ProductSerializer, ProductTypeAttributeSerializer
from django.db.models import Q

from .models import ProductType, TypeAttribute
from .serializers import ProductTypeSerializer


class ProductsAttributesValueViewsets(viewsets.ModelViewSet):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer


class ProductsViewsets(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Only return approved products
        # TODO write tests for this
        return Product.objects.filter(approved=True)


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


class ProductTypeAttributeViewSet(viewsets.ModelViewSet):
    queryset = TypeAttribute.objects.all()
    serializer_class = ProductTypeAttributeSerializer
