from django.db import models
import uuid
from products.models import validate_image
from django.contrib.auth import get_user_model


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="vendor_profile"
    )
    store_name = models.CharField(max_length=255)
    store_address = models.TextField()
    store_bio = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00)
    social_links = models.JSONField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="products", validators=[validate_image], blank=True, null=True
    )

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            avg_rating = ratings.aggregate(models.Avg("rating"))["rating__avg"]
            self.average_rating = round(avg_rating, 2)
            self.save()

    def __str__(self):
        return self.store_name

    def get_vendor_products(self):
        products = self.vendor_products.all()  # .store_name
        # print("store_name:", products)
        return products

    def get_sales_report(self):
        sales = self.transactions.aggregate(total_sales=models.Sum("amount"))
        return sales["total_sales"] if sales["total_sales"] else 0


class VendorDiscount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vendor.name} - {self.discount_percentage}"


class VendorRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="vendor_ratings"
    )
    rating = models.PositiveSmallIntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - review of - {self.vendor.store_name}"


class VendorTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="transactions"
    )
    # order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='vendor_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.store_name} - {self.amount}"
