from django.urls import include, path
from .views import (
    AttributeViewSet,
    AttributeOptionViewSet,
    AttributesValueViewsets,
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()


router.register("attributes", AttributeViewSet, basename="attribute")

router.register("attribute-options", AttributeOptionViewSet, basename="attribute-option")

router.register("attribute-values", AttributesValueViewsets, basename="attribute-value",)
urlpatterns = [
    path("", include(router.urls)),
]
