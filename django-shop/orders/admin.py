from django.contrib import admin

from .models import OrderTracking, Order, OrderItem

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderTracking)