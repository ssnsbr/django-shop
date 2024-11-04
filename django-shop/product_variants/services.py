from django.db import transaction
from .models import ProductVariant, VariantAttributeValue


def create_or_get_variant(product, attribute_ids, name=None):
    # Check for existing variant with the same attributes
    existing_variant = ProductVariant.find_duplicate(product, attribute_ids)
    if existing_variant:
        return existing_variant, False

    # If no duplicate, proceed with creating a new variant
    fingerprint = ProductVariant.get_fingerprint(attribute_ids)
    with transaction.atomic():
        # Create new variant
        new_variant = ProductVariant.objects.create(
            product=product,
            name=name,
            fingerprint=fingerprint,
        )
        # Link the attributes to the new variant
        for attribute_id in attribute_ids:
            VariantAttributeValue.objects.create(
                variant=new_variant, attribute_value_id=attribute_id
            )

    return new_variant, True
