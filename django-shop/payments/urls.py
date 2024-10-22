from django.urls import path
from .views import go_to_gateway_view, callback_gateway_view
from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path("bankgateways/", az_bank_gateways_urls()),
    path("go-to-gateway/", go_to_gateway_view),
    path("callback-gateway/", callback_gateway_view, name="callback-gateway"),
]
