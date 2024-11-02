from django.db import models
from django.urls import reverse
import uuid
from django.core.exceptions import ValidationError
from PIL import Image
# from django_measurement.models import MeasurementField


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
    # weight = MeasurementField(
    #     measurement=Weight,
    #     unit_choices=WeightUnits.CHOICES,
    #     blank=True,
    #     null=True,
    # )
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
    GLOBAL = 1
    LOCAL = 2
    ATTRIBUTE_TYPE_CHOICES = [
        (GLOBAL, 'Global'),
        (LOCAL, 'Local'),
    ]  # global (product-level) and local (variant-level) attributes
    attribute_type = models.PositiveSmallIntegerField(choices=ATTRIBUTE_TYPE_CHOICES)

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


# class ProductVariantManager(models.Manager):
#     def get_or_create_variant(self, product, attributes):
#         # Try to find an existing variant with the same product and attributes
#         existing_variant = self.filter(product=product)
#         print("checking...")
#         for variant in existing_variant:
#             if set(variant.attributes.all()) == set(attributes):
#                 return variant, False  # Variant exists, return it

#         # If not found, create a new variant
#         variant = self.create(product=product)
#         variant.attributes.set(attributes)  # Assign the attributes
#         variant.save()
#         return variant, True  # Variant created


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    attributes = models.ManyToManyField(ProductAttributeValue, related_name="subproducts")
    name = models.CharField(max_length=255)  # Optional, for easy reference
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = ProductVariantManager()  # Use the custom manager

    def __str__(self):
        return f"{self.product.name} - {self.get_attributes_display()}"

    def get_attributes_display(self):
        return ', '.join([f"{attr.attribute.name}: {attr.option}" for attr in self.attributes.all()])

    def clean(self):
        """
        Ensure that only local (variant-level) attributes are assigned to a ProductVariant.
        """
        for attr_value in self.attributes.all():
            if attr_value.attribute.attribute_type != ProductAttribute.LOCAL:
                raise ValidationError(
                    f"The attribute '{attr_value.attribute.name}' is a global attribute and "
                    f"cannot be used in a product variant."
                )

    def save(self, *args, **kwargs):
        self.clean()

        super(ProductVariant, self).save(*args, **kwargs)
        # Create or update a row in the PriceHistory table if the attributes affect price
        # self.update_price_history()

    # def update_price_history(self): TODO
    #     # Get attributes that affect price
    #     price_affecting_attributes = self.attributes.filter(attribute__affects_price=True)

    #     # Check if any price-affecting attributes exist
    #     if price_affecting_attributes.exists():
    #         for listing in self.vendor_listings.all():  # Assuming related name for VendorListing is `vendor_listings`
    #             # Create a new price history entry for each vendor listing of this variant
    #             PriceHistory.objects.create(
    #                 product_variant=self,
    #                 vendor=listing.vendor,
    #                 price=listing.price
    #             )
