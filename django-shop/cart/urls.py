from .views import CartItemViewsets  # , CartViewsets

from rest_framework.routers import SimpleRouter


# urlpatterns = [
#     path("", ProductsList.as_view(), name="product_list"),
#     path("<uuid:pk>/", ProductDetail.as_view(), name="product_detail"),
# ]
router = SimpleRouter()
# router.register("", CartViewsets, basename="cart")
router.register("cart-items", CartItemViewsets, basename="cartitem")

urlpatterns = router.urls
