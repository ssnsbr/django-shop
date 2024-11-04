from .models import ProductVariant, VariantAttributeValue
from rest_framework import serializers

from django.contrib.auth import get_user_model
from products.serializers import ProductSerializer
from products.models import Product

User = get_user_model()


class VariantAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    option_value = serializers.CharField(source='option.value', read_only=True)
    # attributes = AttributeSerializer(many=True, read_only=True)
    # option = AttributeOptionSerializer()

    class Meta:
        model = VariantAttributeValue
        fields = ['attribute_name', 'option_value']
        # fields = "__all__"  # ['option', 'variant']


class ProductVariantSerializer(serializers.ModelSerializer):
    variant_attributes = VariantAttributeValueSerializer(many=True, read_only=True)
    # option = AttributeOptionSerializer(read_only=True, many=True)
    product = ProductSerializer(read_only=True)
    product = serializers.SlugRelatedField(slug_field='id', queryset=Product.objects.all())  # Show product ID
    attributes = serializers.SerializerMethodField("get_attributes")
    attribute = serializers.RelatedField(read_only=True)

    def get_attributes(self, ins):
        data = VariantAttributeValueSerializer(ins.variant_attributes).data
        return data

    class Meta:
        model = ProductVariant
        # fields = "__all__"
        fields = ['id', 'product', 'name', 'created_at', 'updated_at', 'variant_attributes']

    def get_attributes_display(self):
        return ', '.join([f"{attr.attribute.name}: {attr.option.value}" for attr in self.attributes.all()])
