from django.contrib import admin

from .models import ProductVariant, VariantAttributeValue

admin.site.register(ProductVariant)
admin.site.register(VariantAttributeValue)
