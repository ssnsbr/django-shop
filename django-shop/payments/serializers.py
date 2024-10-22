from rest_framework import serializers
from .models import VendorPayment
from django.contrib.auth import get_user_model

User = get_user_model()


class VendorPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPayment
        fields = "__all__"
