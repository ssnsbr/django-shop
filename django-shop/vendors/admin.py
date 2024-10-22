from django.contrib import admin
from .models import Vendor, VendorTransaction, VendorDiscount, VendorRating


admin.site.register(VendorDiscount)
admin.site.register(VendorRating)
admin.site.register(Vendor)
admin.site.register(VendorTransaction)
