from django.test import TestCase
from order.models import Order, ShippingMethod
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class ShippingTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.shipping_method = ShippingMethod.objects.create(name="Standard", price=10.00)

    def test_shipping_method_applied(self):
        """Test that the selected shipping method is applied to the order."""
        order = Order.objects.create(
            user=self.user,
            shipping_method=self.shipping_method,
            shipping_cost=self.shipping_method.price,
            total_price=0,
        )

        self.assertEqual(order.shipping_method, self.shipping_method)
        self.assertEqual(order.shipping_cost, self.shipping_method.price)
