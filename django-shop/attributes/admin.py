from django.contrib import admin

from .models import AttributeValue, AttributeOption, Attribute

admin.site.register(AttributeValue)
admin.site.register(AttributeOption)
admin.site.register(Attribute)
