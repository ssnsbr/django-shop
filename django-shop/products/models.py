import hashlib
from itertools import product
from django.db import models
from django.urls import reverse
import uuid
from django.core.exceptions import ValidationError
from PIL import Image
from attributes.models import Attribute, AttributeValue, AttributeOption
from django.db import transaction


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
    # attributes = models.ManyToManyField(AttributeOption, related_name="ProductAttributeValue")

    name = models.CharField(max_length=255)
    description_text = models.TextField(blank=True, null=True)
    description_json = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
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
        self.generate_all_variants()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])

    def first_image(self):
        all_media = self.media.all()
        return all_media[0] if all_media else None  # TODO '/static/img/default_product.png'

    def generate_all_variants(self):
        product_type = self.product_type
        required_attributes = TypeAttribute.objects.filter(
            product_type=product_type,
            attribute_type=TypeAttribute.VARIANT_ATTRIBUTE,
            is_required=True
        )

        # Gather all options for each required attribute
        attribute_options_map = {}
        for type_attr in required_attributes:
            options = AttributeOption.objects.filter(attribute=type_attr.attribute)
            attribute_options_map[type_attr.attribute] = options

        # Create all possible combinations of options
        attribute_combinations = list(product(*attribute_options_map.values()))

        variants_created = []
        try:
            with transaction.atomic():
                for options_tuple in attribute_combinations:
                    # For each combination, create or retrieve the AttributeValue instances
                    attributes = []
                    for option in options_tuple:
                        attribute = option.attribute
                        attribute_value, created = AttributeValue.objects.get_or_create(
                            attribute=attribute,
                            option=option
                        )
                        attributes.append(attribute_value)

                    # Sort the attributes to ensure uniqueness
                    attributes_sorted = sorted(attributes, key=lambda x: x.attribute.id)

                    # Generate a unique hash for the attributes
                    serialized_attributes = "|".join(f"{attr.attribute.id}:{attr.option.id}" for attr in attributes_sorted)
                    attribute_hash = hashlib.sha256(serialized_attributes.encode()).hexdigest()

                    # Check if a variant with this hash already exists
                    if ProductVariant.objects.filter(product=self, attribute_hash=attribute_hash).exists():
                        continue  # Skip if this variant already exists

                    # Create the new variant
                    variant = ProductVariant(product=self, name=self.name, attribute_hash=attribute_hash)
                    variant.save()
                    variant.attributes.set(attributes)  # Set all attributes at once
                    variant.save()  # Final save to save relationships and hash
                    variants_created.append(variant)
                print("variants_created:", variants_created)

        except ValidationError as e:
            print(f"Validation Error: {e}")

        return variants_created


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


class TypeAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=True)
    """Represents an attribute that can apply to products or variants."""
    PRODUCT_ATTRIBUTE = 1
    VARIANT_ATTRIBUTE = 2
    ATTRIBUTE_TYPE_CHOICES = [
        (PRODUCT_ATTRIBUTE, 'Product Level'),
        (VARIANT_ATTRIBUTE, 'Variant Level'),
    ]

    attribute_type = models.PositiveSmallIntegerField(choices=ATTRIBUTE_TYPE_CHOICES)

    class Meta:
        unique_together = ('product_type', 'attribute')  # Ensures each attribute is assigned once per product type

    def __str__(self):
        req = "Required" if self.is_required else "Optional"
        att_type = "Product Level" if self.attribute_type == TypeAttribute.PRODUCT_ATTRIBUTE else "Variant Level"
        return f"{self.product_type.name} - {self.attribute.name} - {att_type} - {req}"


class ProductAttributeValue(models.Model):
    """Values for global product attributes."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_attributes")
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'attribute_value')

    def __str__(self):
        return f"{self.product.name} - {self.attribute_value.option.attribute.name}: {self.attribute_value.option.value}"

    # def clean(self):
    #     super().clean()  # Call the parent's clean method

    #     # Ensure all attributes are of type
    #     for attr in self.attribute.all():
    #         if attr.attribute_type != Attribute.PRODUCT_ATTRIBUTE:
    #             raise ValidationError(
    #                 f"The attribute '{attr.name}' cannot be used in a product."
    #             )

    # def clean(self):
    #     super().clean()  # Call the parent's clean method
    #     if self.attribute.attribute_type != Attribute.VARIANT_ATTRIBUTE:
    #         raise ValidationError(
    #             f"The attribute '{self.attribute.name}' cannot be used in a variant."
    #         )

    #     existing_value = VariantAttributeValue.objects.filter(
    #         variant__product=self.variant.product,
    #         attribute=self.attribute
    #     ).exclude(variant=self.variant)  # Exclude current variant to allow updates

    #     if existing_value.exists():
    #         raise ValidationError(
    #             f"The attribute '{self.attribute.name}' is already assigned to another variant of this product."
    #         )

    # def save(self, *args, **kwargs):
    #     self.clean()  # Enforce validation rules before saving
    #     super().save(*args, **kwargs)

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
