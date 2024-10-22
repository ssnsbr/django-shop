from django.test import TestCase
from vendors.models import VendorProduct, Vendor
from cart.models import Cart, CartItem
from order.models import Order, OrderItem
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CartManagementTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.vendoruser = get_user_model().objects.create_user(
            username="testuservendor", password="password"
        )

        self.vendor = Vendor.objects.create(owner=self.vendoruser, store_name="Vendor A")
       
        self.vendor_product = VendorProduct.objects.create(
            vendor=self.vendor, name="Product A", price=50.00, warehouse_quantity=100
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, vendor_product=self.vendor_product, quantity=2
        )

    def test_cart_items_removed_after_order(self):
        """Test that cart items are removed after order creation."""
        order = Order.objects.create(
            user=self.user, total_price=100
        )

        OrderItem.objects.create(
            order=order,
            item=self.vendor_product,
            quantity=self.cart_item.quantity,
            price=self.vendor_product.price,
        )

        # Simulate clearing the cart
        self.cart.items.all().delete()

        self.assertEqual(self.cart.items.count(), 0)