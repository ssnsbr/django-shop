from rest_framework import serializers
from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):  # new
    class Meta:
        model = CartItem
        # fields = ["vendor_product"]
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):  # new
    class Meta:
        model = Cart
        fields = "__all__"
