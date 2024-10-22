
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

"""
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


urlpatterns = [
    path("anything-but-admin/", admin.site.urls),
    # path("api/cart/", include("cart.urls")),
    path("api/", include("products.urls")),
    path("api/vendors/", include("vendors.urls")),
    # path("api/", include("vendor_products.urls")),
    # path("api/orders/", include("order.urls")),
    # path("api/payment/", include("payment.urls")),
    # path("api/", include("search.urls")),
    # path("users/", include("django.contrib.auth.urls")),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path(
        "api/dj-rest-auth/registration/",
        include("dj_rest_auth.registration.urls"),
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
