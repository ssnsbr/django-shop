from django.urls import include, path
from .views import (
    ProductsAttributesValueViewsets,
    ProductsMediaViewsets,
    ProductsViewsets,
    ProductTypeViewSet,
    ProductTypeAttributeViewSet
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("product", ProductsViewsets, basename="product")
router.register(
    "products/<uuid:pk>/media", ProductsMediaViewsets, basename="product-media"
)

router.register("product-types", ProductTypeViewSet, basename="product-type")
router.register(
    "product-type-attributes",
    ProductTypeAttributeViewSet,
    basename="product-type-attribute",
)
router.register(
    "product-attribute-values",
    ProductsAttributesValueViewsets,
    basename="product-attribute-value",
)
urlpatterns = [
    path("", include("product_variants.urls")),
    path("", include(router.urls)),
]
