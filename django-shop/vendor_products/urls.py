from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vendor_products.views import VendorProductViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'vendor-products', VendorProductViewSet, basename='vendor-products')

urlpatterns = [
    path('', include(router.urls)),
]
