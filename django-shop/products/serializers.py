from .models import (Product, ProductMedia,
                     ProductType,
                     ProductAttribute,
                     ProductTypeAttribute,
                     ProductAttributeValue,
                     )
from rest_framework import serializers

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
        fields = ["id", "name", "slug", "description", "created_at", "updated_at"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["id", "name", "description"]


class ProductTypeAttributeSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer(read_only=True)
    attribute = ProductAttributeSerializer(read_only=True)

    class Meta:
        model = ProductTypeAttribute
        fields = ["product_type", "attribute", "is_required"]


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field="name"
    )
    attribute = ProductAttributeSerializer(read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ["product", "attribute", "value"]


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
