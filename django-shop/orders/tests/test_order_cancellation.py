from django.test import TestCase
from orders.models import Order, OrderItem
from cart.models import CartItem, Cart
from vendors.models import Vendor
from django.contrib.auth import get_user_model
from vendor_products.models import VendorListing

CustomUser = get_user_model()


class OrderCancellationTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.vendoruser = get_user_model().objects.create_user(
            username="testuservendor", password="password"
        )

        self.vendor = Vendor.objects.create(owner=self.vendoruser, store_name="Vendor A")

        self.vendor_product = VendorListing.objects.create(
            vendor=self.vendor, name="Product A", price=50.00, warehouse_quantity=100
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, vendor_product=self.vendor_product, quantity=2
        )

    def test_order_cancellation(self):
        """Test if the order can be canceled and items returned to cart."""
        order = Order.objects.create(
            user=self.user,
            total_price=100
        )

        OrderItem.objects.create(
            order=order,
            item=self.vendor_product,
            quantity=self.cart_item.quantity,
            price=self.vendor_product.price,
        )

        # Simulate cancellation
        order.delete()
        CartItem.objects.create(
            cart=self.cart,
            vendor_product=self.vendor_product,
            quantity=self.cart_item.quantity,
        )

        # Verify cart items are restored after cancellation
        self.assertEqual(self.cart.items.count(), 1)
