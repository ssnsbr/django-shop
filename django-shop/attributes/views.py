from rest_framework import viewsets
from .models import Attribute, AttributeOption, AttributeValue
from .serializers import AttributeOptionSerializer, AttributeSerializer, AttributeValueSerializer


class AttributeOptionViewSet(viewsets.ModelViewSet):
    queryset = AttributeOption.objects.all()
    serializer_class = AttributeOptionSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributesValueViewsets(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
