from django.test import TestCase
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from vendors.models import VendorProduct, Vendor
from order.models import Order, OrderItem, ShippingMethod, UserAddress

CustomUser = get_user_model()

class OrderCreationTests(TestCase):
    def setUp(self):
        # Set up common data
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
        self.shipping_method = ShippingMethod.objects.create(name="Standard", price=10.00)
        self.address = UserAddress.objects.create(
            user=self.user,
            street="123 Test St",
            city="Test City",
            postal_code="12345",
            country="Test Country"
        )

    def test_order_creation_from_cart(self):
        """Test successful creation of an order from cart items."""
        order = Order.objects.create(
            user=self.user,
            shipping_method=self.shipping_method,
            shipping_cost=self.shipping_method.price,
            address=self.address,
            total_price=0,
        )

        OrderItem.objects.create(
            order=order,
            item=self.vendor_product,
            quantity=self.cart_item.quantity,
            price=self.vendor_product.price,
        )

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.get_total_cost(), 110.00)
        self.assertEqual(order.shipping_method, self.shipping_method)
        self.assertEqual(order.address, self.address)
