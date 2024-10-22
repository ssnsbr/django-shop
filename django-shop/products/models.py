from django.db import models
from django.urls import reverse
import uuid
from django.core.exceptions import ValidationError
from PIL import Image


# Category model to categorize products
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    description_text = models.TextField(blank=True)
    description_json = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )

    background_image = models.ImageField(
        upload_to="category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    product_type = models.ForeignKey(
        ProductType, on_delete=models.SET_NULL, null=True, related_name="products"
    )

    name = models.CharField(max_length=255)
    description_text = models.TextField(blank=True, null=True)
    description_json = models.TextField(blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(null=True, blank=True)

    @staticmethod
    def available_products():
        return Product.objects.filter(vendor_products__available=True).distinct()

    @staticmethod
    def filter_by_price(min_price, max_price):
        return Product.objects.filter(
            vendor_products__price__gte=min_price, vendor_products__price__lte=max_price
        ).distinct()

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = slugify(self.name+self.id)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])

    def first_image(self):
        all_media = self.media.all()
        return all_media[0] if all_media else None  # TODO '/static/img/default_product.png'


def validate_image(image):
    try:
        img = Image.open(image)
        img.verify()
    except Exception:
        raise ValidationError("Uploaded file is not a valid image.")


class ProductMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        related_name="media",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to="products", validators=[validate_image], blank=True, null=True
    )
    alt = models.CharField(max_length=250, blank=True)
    external_url = models.CharField(max_length=256, blank=True, null=True)


################################################################################
################################################################################


class ProductAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductAttributeOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name="options")
    value = models.CharField(max_length=255)  # e.g., "XS", "S", "M", "L", etc.

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductTypeAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_type.name} - {self.attribute.name}"


class ProductAttributeValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductAttributeOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.option.value}"


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="subproducts"
    )
    attributes = models.ManyToManyField(ProductAttributeValue, related_name="subproducts")
    name = models.CharField(max_length=255)  # Optional, for easy reference
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.get_attributes_display()}"

    def get_attributes_display(self):
        return ', '.join([f"{attr.attribute.name}: {attr.value}" for attr in self.attributes.all()])
