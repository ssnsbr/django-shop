from decimal import Decimal
from typing import Any, Dict
from uuid import UUID
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from products.serializers import ProductMediaSerialiser
from vendor_products.models import VendorProduct


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


class VendorProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField("get_vendor_name")
    product_name = serializers.SerializerMethodField("get_product_name")
    product_image = serializers.SerializerMethodField("get_product_image")

    # @extend_schema_field(serializers.JSONField)
    def get_product_image(self, obj) -> Dict[str, Any]:
        data = ProductMediaSerialiser(obj.product.first_image()).data
        return data

    @extend_schema_field(serializers.CharField)
    def get_vendor_name(self, obj) -> Dict[str, Any]:
        print(":", obj)
        try:
            return obj.vendor.store_name
        except Exception:
            return True

    @extend_schema_field(serializers.CharField)
    def get_product_name(self, obj) -> Dict[str, Any]:
        # print("vendor_name: obj:",obj)
        # data = VendorSerializer(obj.store_name()).data
        return obj.product.name

    def validate_uuid(self, value):
        print("UUID")
        if is_valid_uuid(value):
            return value
        else:
            raise serializers.ValidationError(str(value) + " is not a valid UUID..")

    def validate_id(self, value):
        if is_valid_uuid(value):
            return value
        else:
            raise serializers.ValidationError(str(value) + " is not a valid UUID..")

    def validate_price(self, value):
        """
        Check that the price is a valid Decimal and not less than zero.
        """
        if value is None:
            raise serializers.ValidationError("Price is required.")
        if not isinstance(value, Decimal):
            raise serializers.ValidationError(
                "Price must be a Decimal, not " + value.__class__.__name__
            )
        if value < 0:
            raise serializers.ValidationError(
                "Price must be greater than or equal to 0."
            )
        return value

    class Meta:
        model = VendorProduct
        # fields =
        fields = "__all__"
        extra_fields = ["vendor_name", "product_name"]


class VendorProductListSerializer(serializers.ListSerializer):
    child = VendorProductSerializer()
