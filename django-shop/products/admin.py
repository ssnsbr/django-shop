from django.contrib import admin

from .models import (
    Category,
    Product,
    TypeAttribute,
    ProductType
)


admin.site.register(TypeAttribute)
admin.site.register(ProductType)

admin.site.register(Category)
admin.site.register(Product)
