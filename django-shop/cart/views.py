from rest_framework.response import Response
from rest_framework import viewsets, status
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated


class CartViewsets(viewsets.ReadOnlyModelViewSet):  # read only
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    # http_method_names = ["get"] or ReadOnlyModelViewSet

    def get_queryset(self):
        print("CartViewsets get_queryset")

        # Return only the cart of the authenticated user
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        print("CartViewsets get_object")
        # Get or create the cart for the authenticated user
        obj, created = Cart.objects.get_or_create(user=self.request.user)
        print("CartViewsets get_object", obj, created)

        return obj


class CartItemViewsets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    # queryset = CartItem.objects.all()

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def update(self, request, pk=None):
        print("CartItemViewsets update")
        return self.create(request)

    def create(self, request, *args, **kwargs):
        print("CartItemViewsets", request.user, *args, **kwargs)
        vendor_product = request.data.get("vendor_product")
        cart, created = Cart.objects.get_or_create(user=request.user)
        print("leo test in create")

        # Ensure vendor_product is provided
        if not vendor_product:
            return Response(
                {"error": "vendor_product is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the item already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, vendor_product_id=vendor_product, defaults={"quantity": 1}
        )

        if not created:
            # If the item already exists, increase the quantity
            cart_item.quantity += 1
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
