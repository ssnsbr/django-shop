from .models import AttributeOption, Attribute, AttributeValue
from rest_framework import serializers


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"


class AttributeOptionSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = AttributeOption
        fields = "__all__"


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    option_value = serializers.CharField(source='option.value', read_only=True)

    class Meta:
        model = AttributeValue
        fields = ['attribute_name', 'option_value']
