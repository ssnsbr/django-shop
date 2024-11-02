from django.urls import include, path
from .views import (
    ProductsMediaViewsets,
    ProductsViewsets,
    ProductTypeViewSet,
    ProductAttributeViewSet,
    ProductTypeAttributeViewSet,
    ProductAttributeValueViewSet, ProductsVariantViewsets
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("product", ProductsViewsets, basename="product")
router.register(
    "products/<uuid:pk>/media", ProductsMediaViewsets, basename="product-media"
)
router.register("product-variants", ProductsVariantViewsets, basename="product-vaiant")

router.register("product-types", ProductTypeViewSet, basename="product-type")
router.register(
    "product-attributes", ProductAttributeViewSet, basename="product-attribute"
)
router.register(
    "product-type-attributes",
    ProductTypeAttributeViewSet,
    basename="product-type-attribute",
)
router.register(
    "product-attribute-values",
    ProductAttributeValueViewSet,
    basename="product-attribute-value",
)

urlpatterns = [
    path("", include(router.urls)),
]
