import hashlib
from django.db import IntegrityError, models
import uuid
from products.models import Product
from django.core.exceptions import ValidationError
from attributes.models import AttributeValue


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    name = models.CharField(max_length=255)  # Optional, for easy reference
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fingerprint = models.CharField(max_length=64, editable=False, unique=True)

    def __str__(self):
        return f"{self.product.name} "  # - {self.get_attributes_display()}

    def save(self, *args, **kwargs):
        self.clean()
        try:
            super(ProductVariant, self).save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError("A variant with identical attributes already exists.")

    @staticmethod
    def get_fingerprint(attribute_ids):
        """Generate a fingerprint based on sorted attribute IDs."""
        sorted_ids = sorted(attribute_ids)
        concatenated_ids = "-".join(map(str, sorted_ids))
        return hashlib.sha256(concatenated_ids.encode()).hexdigest()

    @classmethod
    def find_duplicate(cls, product, attribute_ids):
        """Check if a variant with the same attributes already exists."""
        fingerprint = cls.get_fingerprint(attribute_ids)
        return cls.objects.filter(product=product, fingerprint=fingerprint).first()


class VariantAttributeValue(models.Model):
    """Values for local variant attributes."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_attributes")
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('variant', 'attribute_value')

    def __str__(self):
        return f"{self.variant.product.name} (Variant) - {self.attribute_value.option.attribute.name}: {self.attribute_value.option.value}"
