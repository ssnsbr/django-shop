
import uuid
from django.db import models
from django.contrib.auth import get_user_model

from users.models import UserAddress
from vendor_products.models import VendorListing
from vendors.models import Vendor

CustomUser = get_user_model()


class ShippingMethod(models.Model):
    name = models.CharField(
        max_length=100
    )  # Shipping method name (e.g., "Standard", "Express")
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Flat cost of the shipping method

    def __str__(self):
        return self.name


# Create your models here.
class Order(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # address = models.CharField(max_length=250)  # TODO
    # city = models.CharField(max_length=100)
    shipping_method = models.ForeignKey(
        ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True
    )
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.ForeignKey(
        UserAddress, on_delete=models.SET_NULL, null=True, blank=True
    )  # Foreign key to UserAddress

    paid = models.BooleanField(default=False)

    provider = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="vendor_provider"
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + self.shipping_cost


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    item = models.ForeignKey(
        VendorListing, related_name="order_items", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def get_cost(self):
        return self.price * self.quantity

    def vendor(self):
        return self.item.vendor


class OrderTracking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="tracking"
    )
    # Existing fields...
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Canceled", "Canceled"),
        ("Shipped", "Shipped"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    updated_at = models.DateTimeField(auto_now=True)
    cancellation_requested = models.BooleanField(default=False)
    cancellation_approved = models.BooleanField(default=False)
    refund_processed = models.BooleanField(
        default=False
    )  # Flag to indicate if refund has been processed
    details = models.TextField(
        blank=True, null=True
    )  # Additional information about the status change
