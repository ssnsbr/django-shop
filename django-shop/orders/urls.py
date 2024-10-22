from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CreateOrderFromCartView

# Create a router and register the order viewset
order_router = SimpleRouter()
order_router.register(r'orders', CreateOrderFromCartView, basename='order')

urlpatterns = [
    path('', include(order_router.urls)),
    # Additional order-related URLs can be placed here
]

# urlpatterns = [
#     # URL for creating an order from the cart
#     path('create-order/', CreateOrderFromCartView.as_view({'post': 'create'}), name='create_order'),

#     # URL for canceling an order
#     path('cancel-order/<int:pk>/', CancelOrderView.as_view(), name='cancel_order'),

#     # URL for listing a user's orders
#     path('orders/', OrderListView.as_view(), name='order_list'),
# ]
