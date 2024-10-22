from django.test import TestCase
from vendors.models import Vendor, VendorProduct
from order.models import Order, ShippingMethod, UserAddress
from cart.models import Cart, CartItem
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class OrderSplitTests(TestCase):
    def setUp(self):
        # Set up common data
        self.user = CustomUser.objects.create(username="testuser")
        
        # Vendor A and products
        self.vendor_a = Vendor.objects.create(name="Vendor A")
        self.vendor_product_a = VendorProduct.objects.create(
            vendor=self.vendor_a, name="Product A", price=50.00, warehouse_quantity=100
        )
        
        # Vendor B and products
        self.vendor_b = Vendor.objects.create(name="Vendor B")
        self.vendor_product_b = VendorProduct.objects.create(
            vendor=self.vendor_b, name="Product B", price=30.00, warehouse_quantity=50
        )

        # Cart and items
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item_a = CartItem.objects.create(
            cart=self.cart, vendor_product=self.vendor_product_a, quantity=2
        )
        self.cart_item_b = CartItem.objects.create(
            cart=self.cart, vendor_product=self.vendor_product_b, quantity=1
        )
        
        self.shipping_method = ShippingMethod.objects.create(name="Standard", price=10.00)
        self.address = UserAddress.objects.create(
            user=self.user, street="123 Test St", city="Test City", postal_code="12345", country="Test Country"
        )

    def test_order_split_by_vendor(self):
        """Test that orders are split by vendor correctly."""
        # Assume method to create orders
        orders = self.view.create_order(
            shipping_method_id=self.shipping_method.id, address_id=self.address.id
        )

        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0].items.count(), 1)  # Vendor A's product
        self.assertEqual(orders[1].items.count(), 1)  # Vendor B's product
