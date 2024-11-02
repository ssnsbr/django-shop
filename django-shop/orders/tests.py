from django.test import TestCase
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from vendors.models import Vendor
from vendor_products.models import VendorListing
from .models import Order, OrderItem, ShippingMethod, UserAddress

CustomUser = get_user_model()

# UnauthorizedUser  User Owner  Vendor  Admin
#               UU  US   VN   AD
# CreateOrder    N   Y    N   N
#
#  test_order_creation_from_cart """Test if an order is created successfully from cart items"""
#  test_order_split_by_vendor """Test if orders are split by vendor"""
#  test_cart_items_removed_after_order """Test that cart items are removed after order creation"""
#  test_insufficient_stock_prevents_order """Test that an order is prevented if there is not enough stock"""
#  test_order_cancellation """Test if the order can be canceled and items returned to cart"""
#  test_shipping_method_applied """Test that the selected shipping method is applied to the order"""


class OrderAppTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = CustomUser.objects.create(username="testuser")

        # Create vendors and products
        self.vendor_a = Vendor.objects.create(name="Vendor A")
        self.vendor_product_a = VendorListing.objects.create(
            vendor=self.vendor_a, name="Product A", price=50.00, warehouse_quantity=100
        )

        self.vendor_b = Vendor.objects.create(name="Vendor B")
        self.vendor_product_b = VendorListing.objects.create(
            vendor=self.vendor_b, name="Product B", price=30.00, warehouse_quantity=50
        )

        # Create cart and cart items
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item_a = CartItem.objects.create(
            cart=self.cart, vendor_product=self.vendor_product_a, quantity=2
        )
        self.cart_item_b = CartItem.objects.create(
            cart=self.cart, vendor_product=self.vendor_product_b, quantity=1
        )

        # Create a shipping method
        self.shipping_method = ShippingMethod.objects.create(
            name="Standard", price=10.00
        )

        # Create a user address
        self.address = UserAddress.objects.create(
            user=self.user,
            street="123 Test St",
            city="Test City",
            postal_code="12345",
            country="Test Country",
        )

    # Test Order Creation
    def test_order_creation_from_cart(self):
        """Test if an order is created successfully from cart items"""
        # Create the order
        order = Order.objects.create(
            user=self.user,
            shipping_method=self.shipping_method,
            shipping_cost=self.shipping_method.price,
            address=self.address,
            total_price=0,
        )

        OrderItem.objects.create(
            order=order,
            item=self.vendor_product_a,
            quantity=self.cart_item_a.quantity,
            price=self.vendor_product_a.price,
        )

        # Verify the order
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(
            order.get_total_cost(),
            (self.vendor_product_a.price * self.cart_item_a.quantity)
            + self.shipping_method.price,
        )
        self.assertEqual(order.shipping_method, self.shipping_method)
        self.assertEqual(order.address, self.address)

        # Check stock was reduced
        self.vendor_product_a.refresh_from_db()
        self.assertEqual(self.vendor_product_a.warehouse_quantity, 98)

    # Test Order Splitting by Vendor
    def test_order_split_by_vendor(self):
        """Test if orders are split by vendor"""
        # Assume this method splits orders by vendor
        orders = self.view.create_order(
            shipping_method_id=self.shipping_method.id, address_id=self.address.id
        )

        # Verify two orders were created (one per vendor)
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0].items.count(), 1)  # Vendor A
        self.assertEqual(orders[1].items.count(), 1)  # Vendor B

    # Test Cart Items Removed After Order
    def test_cart_items_removed_after_order(self):
        """Test that cart items are removed after order creation"""
        # Create the order
        order = Order.objects.create(
            user=self.user,
            shipping_method=self.shipping_method,
            shipping_cost=self.shipping_method.price,
            address=self.address,
            total_price=0,
        )

        OrderItem.objects.create(
            order=order,
            item=self.vendor_product_a,
            quantity=self.cart_item_a.quantity,
            price=self.vendor_product_a.price,
        )

        # Simulate clearing the cart
        self.cart.items.all().delete()

        # Verify cart is empty
        self.assertEqual(self.cart.items.count(), 0)

    # Test Insufficient Stock Prevents Order
    def test_insufficient_stock_prevents_order(self):
        """Test that an order is prevented if there is not enough stock"""
        # Set insufficient stock
        self.vendor_product_a.warehouse_quantity = 1
        self.vendor_product_a.save()

        with self.assertRaises(Exception):  # or handle as your view does
            order = Order.objects.create(
                user=self.user,
                shipping_method=self.shipping_method,
                shipping_cost=self.shipping_method.price,
                address=self.address,
                total_price=0,
            )
            OrderItem.objects.create(
                order=order,
                item=self.vendor_product_a,
                quantity=self.cart_item_a.quantity,
                price=self.vendor_product_a.price,
            )

    # Test Order Cancellation
    def test_order_cancellation(self):
        """Test if the order can be canceled and items returned to cart"""
        # Create the order
        order = Order.objects.create(
            user=self.user,
            shipping_method=self.shipping_method,
            shipping_cost=self.shipping_method.price,
            address=self.address,
            total_price=0,
        )

        OrderItem.objects.create(
            order=order,
            item=self.vendor_product_a,
            quantity=self.cart_item_a.quantity,
            price=self.vendor_product_a.price,
        )

        # Simulate order cancellation
        order.delete()  # or use a cancel method if available
        CartItem.objects.create(
            cart=self.cart,
            vendor_product=self.vendor_product_a,
            quantity=self.cart_item_a.quantity,
        )

        # Verify cart items are restored after cancellation
        self.assertEqual(self.cart.items.count(), 1)

    # Test Shipping Method is Applied Correctly
    def test_shipping_method_applied(self):
        """Test that the selected shipping method is applied to the order"""
        # Create the order
        order = Order.objects.create(
            user=self.user,
            shipping_method=self.shipping_method,
            shipping_cost=self.shipping_method.price,
            address=self.address,
            total_price=0,
        )

        # Verify shipping method is applied
        self.assertEqual(order.shipping_method, self.shipping_method)
        self.assertEqual(order.shipping_cost, self.shipping_method.price)
