from django.urls import include, path
from .views import ProductsVariantViewsets, VariantAttributeValueViewsets
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("variant-attributes", VariantAttributeValueViewsets, basename="variant-attribute")

# router.register(
#     "variants", ProductsVariantViewsets, basename="variant"
# )

urlpatterns = [
    path("", include(router.urls)),
    path("products/<uuid:product_id>/variants/", ProductsVariantViewsets.as_view({"post": "create"}), name="product-variants"),

]
