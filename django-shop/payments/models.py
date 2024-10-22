import uuid
from django.db import models
from django.contrib.auth import get_user_model

from orders.models import Order
from vendors.models import Vendor
from azbankgateways.models import Bank

CustomUser = get_user_model()


class Checkout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    transaction = models.ForeignKey(Bank, on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="users_payment"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orders_payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    success = models.BooleanField(default=False)
    status = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user) + str(self.status)


class Refund(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.OneToOneField(Checkout, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    RefundStatusChoices = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Canceled", "Canceled"),
    ]
    status = models.CharField(max_length=20, choices=RefundStatusChoices)

    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class VendorPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="vednor_payment"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    success = models.BooleanField(default=False)
    VENDOR_PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Canceled", "Canceled"),
    ]
    status = models.CharField(max_length=255, choices=VENDOR_PAYMENT_STATUS_CHOICES)
    description = models.CharField(max_length=255)


# Pk
# Status
# Bank
# Tracking code
# Amount
# 12	Unknown error acquired	PayV1	2947906003112375	10000
#
# Reference number
# Bank result
# Callback url
# Extra information
# Bank choose identifier
# dZeRrJ4		/api/payment/bankgateways/sample-result/	-	1
#
# Created at
# Updated at
# Oct. 5, 2024, 12:49 p.m.	Oct. 5, 2024, 12:49 p.m.

# Extra information:
# {
#     "status": 1,
#     "amount": "10000",
#     "transId": 85090,
#     "factorNumber": "9298538416761060",
#     "mobile": "+989112223344",
#     "description": null,
#     "cardNumber": "123456******1234",
#     "traceNumber": "123",
#     "message": "OK",
# }
