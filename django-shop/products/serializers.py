from .models import (Product, ProductAttributeValue, ProductMedia,
                     ProductType,
                     TypeAttribute

                     )
from rest_framework import serializers
from attributes.serializers import AttributeSerializer
from django.contrib.auth import get_user_model
from typing import Dict, Any


User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField("get_first_image")

    def get_first_image(self, ins) -> Dict[str, Any]:
        data = ProductMediaSerialiser(ins.first_image()).data
        return {"image_url": data["image_url"], "image": data["image"]}

    class Meta:
        model = Product
        # fields = ['id', 'username', 'email']
        fields = "__all__"
        extra_fields = ["first_image"]


class ProductMediaSerialiser(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = ProductMedia
        fields = "__all__"
        extra_fields = ["image_url"]

    # @extend_schema_field(serializers.ImageField)
    def get_image_url(self, obj) -> Dict[str, Any]:
        return obj.image.url


class ProductMediaListSerializer(serializers.ListSerializer):
    child = ProductMediaSerialiser()


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class ProductTypeAttributeSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer(read_only=True)
    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = TypeAttribute
        fields = ["product_type", "attribute", "is_required"]


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    option_value = serializers.CharField(source='option.value', read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ['attribute_name', 'option_value']
    # product = serializers.SlugRelatedField(
    #     queryset=Product.objects.all(), slug_field="name"
    # )
    # attribute = ProductAttributeSerializer(read_only=True)
    # option = ProductAttributeOptionSerializer(read_only=True)
        # fields = ["product", "attribute", "option"]


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

#     def validate(self, data):
#         product_type = data.get('product_type')
#         product = self.instance if self.instance else None
#         provided_attributes = data.get('attributes', [])

#         # Get required attributes for the product type
#         required_attributes = ProductTypeAttribute.objects.filter(
#             product_type=product_type, is_required=True
#         )

#         # Check if all required attributes have been provided
#         missing_attributes = []
#         provided_attr_ids = [attr.attribute.id for attr in provided_attributes]

#         for req_attr in required_attributes:
#             if req_attr.attribute.id not in provided_attr_ids:
#                 missing_attributes.append(req_attr.attribute.name)

#         if missing_attributes:
#             raise serializers.ValidationError(
#                 f"The following required attributes are missing: {', '.join(missing_attributes)}"
#             )

#         return data


# class VariantAttributeValueSerializer(serializers.ModelSerializer):
#     # attribute = serializers.CharField(source='attribute.name', read_only=True)
#     # option = AttributeOptionSerializer(read_only=True, many=True)
#     attributes = AttributeSerializer(many=True, read_only=True)
#     option = AttributeOptionSerializer()

#     class Meta:
#         model = VariantAttributeValue
#         fields = "__all__"  # ['option', 'variant']
#     # product = serializers.SlugRelatedField(


# class ProductVariantSerializer(serializers.ModelSerializer):
    # attribute = VarinatAttributeValueSerializer(read_only=True)
    # variant_attributes = VariantAttributeValueSerializer(many=True, read_only=True)
    # option = AttributeOptionSerializer(read_only=True, many=True)
    # product = ProductSerializer(read_only=True)
    # product = serializers.SlugRelatedField(slug_field='id', queryset=Product.objects.all())  # Show product ID
    # attributes = serializers.SerializerMethodField("get_attributes")
    # attribute = serializers.RelatedField( read_only=True)

    # def get_attributes(self, ins):
    #     data = VariantAttributeValueSerializer(ins.variant_attributes).data
    #     return data

    # class Meta:
    #     model = ProductVariant
    #     # fields = "__all__"
    #     # extra_fields = ['product', "attributes", "option"]
    #     fields = ['id', 'product', 'name', 'created_at', 'updated_at', 'variant_attributes']

    # def get_attributes_display(self):
    #     return ', '.join([f"{attr.attribute.name}: {attr.option.value}" for attr in self.attributes.all()])
