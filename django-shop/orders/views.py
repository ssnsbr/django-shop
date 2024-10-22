from rest_framework import viewsets

from users.models import UserAddress
from cart.models import Cart
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem, OrderTracking, ShippingMethod
from .serializers import OrderSerializer


class CreateOrderFromCartView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.user())

    def user(self):
        return self.request.user

    def create_order(self, shipping_method_id, address_id):
        cart = Cart.objects.get(user=self.user())  # Get user's cart
        orders_list = []
        # total_amount = 0

        try:
            shipping_method = ShippingMethod.objects.get(id=shipping_method_id)
            user_address = UserAddress.objects.get(id=address_id)
        except ShippingMethod.DoesNotExist:
            return Response(
                {"error": "Invalid shipping method."}, status=status.HTTP_400_BAD_REQUEST
            )
        except UserAddress.DoesNotExist:
            return Response(
                {"error": "Invalid address."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Group items by vendor
        vendors = set(item.vendor_product.vendor for item in cart.items.all())

        with transaction.atomic():  # Ensure atomicity
            for vendor in vendors:
                # Create an order for each vendor
                vendor_items = cart.items.filter(vendor_product__vendor=vendor)
                order = Order.objects.create(
                    user=self.user(),
                    total_price=0,  # Initial total is 0
                    shipping_method=shipping_method,
                    shipping_cost=shipping_method.price,
                    address=user_address,
                    paid=False,  # Will be updated once the user completes the payment
                    provider=vendor,  # Assign the vendor as provider
                )

                vendor_total = 0

                # Loop through the vendor's items and create order items
                for cart_item in vendor_items:
                    vendor_product = cart_item.vendor_product

                    # Check stock availability
                    if vendor_product.warehouse_quantity < cart_item.quantity:
                        return Response(
                            {"error": f"Not enough stock for {vendor_product.name}"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # Create an order item for this product
                    order_item = OrderItem.objects.create(
                        order=order,
                        item=vendor_product,
                        quantity=cart_item.quantity,
                        price=vendor_product.price,
                    )

                    # Update stock for this product
                    vendor_product.warehouse_quantity -= cart_item.quantity
                    vendor_product.save()

                    # Add the cost of this item to the vendor's order total
                    vendor_total += order_item.get_cost()

                # Set the total price for the vendor's order (items + shipping)
                order.total_price = vendor_total + shipping_method.price
                order.save()

                # Track order creation in OrderTracking model
                OrderTracking.objects.create(
                    order=order,
                    status="Pending",
                )

                # Add to the list of orders
                orders_list.append(order)

            # Clear the cart after all vendor orders are created
            cart.items.all().delete()

        return orders_list

    def cancel_order(self, order):
        """Return items from the order to the cart if canceled"""
        cart = Cart.objects.get(user=self.user())

        # Move order items back to cart
        for order_item in order.items.all():
            cart.add_item(order_item.item, order_item.quantity)

        # Set order status to 'Canceled'
        order.tracking.status = "Canceled"
        order.tracking.cancellation_requested = True
        order.tracking.save()

    def post(self, request):
        shipping_method_id = request.data.get("shipping_method_id")
        address_id = request.data.get("address_id")

        if not shipping_method_id or not address_id:
            return Response(
                {"error": "Shipping method and address are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        orders_list = self.create_order(shipping_method_id, address_id)

        if isinstance(orders_list, Response):  # Handle potential errors
            return orders_list

        # Return the order details
        serializer = OrderSerializer(orders_list, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """Handle order cancellation"""
        try:
            order = Order.objects.get(pk=pk, user=self.user())
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if order.tracking.status == "Pending" or order.tracking.status == "Paid":
            # Human action required if order is already paid
            if order.tracking.status == "Paid":
                order.tracking.cancellation_requested = True
                order.tracking.save()
                return Response(
                    {
                        "message": "Order cancellation requested. It needs to be approved by an administrator."
                    },
                    status=status.HTTP_200_OK,
                )

            # Cancel the order and return items to the cart
            self.cancel_order(order)
            return Response(
                {"message": "Order canceled, items returned to cart."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Cannot cancel an order that is already shipped."},
            status=status.HTTP_400_BAD_REQUEST,
        )
