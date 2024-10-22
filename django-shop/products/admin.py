from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductAttribute,
    ProductTypeAttribute,
    ProductType,
    ProductAttributeValue,
)


admin.site.register(ProductAttribute)
admin.site.register(ProductTypeAttribute)
admin.site.register(ProductType)
admin.site.register(ProductAttributeValue)

admin.site.register(Category)
admin.site.register(Product)
