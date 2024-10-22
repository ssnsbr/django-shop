from rest_framework import serializers

from vendor_products.serializers import VendorListingSerializer
from .models import Vendor, VendorRating, VendorTransaction
from typing import List, Dict, Any


class VendorSerializer(serializers.ModelSerializer):
    # user = Vendor(read_only=True)
    # vendor_products = serializers.SerializerMethodField("get_vendor_products")
    vendor_products = serializers.SerializerMethodField()

    def get_vendor_products(self, obj) -> List[Dict[str, Any]]:
        products = obj.get_vendor_products()
        return VendorListingSerializer(products, many=True).data

    class Meta:
        model = Vendor
        fields = "__all__"
        extra_fields = ["vendor_products"]


class VendorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRating
        fields = "__all__"


class VendorRatingListSerializer(serializers.ListSerializer):
    child = VendorRatingSerializer()


class VendorTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorTransaction
        fields = "__all__"


class VendorTransactionListSerializer(serializers.ListSerializer):
    child = VendorTransactionSerializer()
