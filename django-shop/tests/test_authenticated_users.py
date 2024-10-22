from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from order.models import Order
from vendor_products.models import VendorListing
from vendors.models import Vendor
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class AuthenticatedUserTests(APITestCase):

    def setUp(self):
        # Create users, products, and carts for testing
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        self.vendoruser = CustomUser.objects.create_user(
            username="testuservendor", password="password"
        )

        self.vendor = Vendor.objects.create(owner=self.vendoruser, store_name="Test Vendor")
        self.product = VendorListing.objects.create(
            name="Test Product", price=100.00, warehouse_quantity=50, vendor=self.vendor
        )
        self.cart_url = reverse("cart-detail")
        self.checkout_url = reverse("checkout")
        self.review_url = reverse("product-review", args=[self.product.id])

    def test_authenticated_user_can_view_product_details(self):
        """Ensure authenticated users can view product details."""
        url = reverse("product-detail", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_view_vendor_details(self):
        """Ensure authenticated users can view vendor details."""
        url = reverse("vendor-detail", args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_view_vendor_warehouse_quantity(self):
        """Ensure authenticated users can view vendor's warehouse quantity."""
        url = reverse("vendorproduct-detail", args=[self.product.id])
        response = self.client.get(url)
        self.assertIn("warehouse_quantity", response.data)

    def test_authenticated_user_can_view_vendor_personal_info(self):
        """Ensure authenticated users can view vendor's personal information."""
        url = reverse("vendor-detail", args=[self.vendor.id])
        response = self.client.get(url)
        self.assertIn("phone", response.data)

    def test_authenticated_user_can_add_to_cart(self):
        """Ensure authenticated users can add items to their own cart."""
        url = reverse("cart-add", args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_access_others_cart(self):
        """Ensure authenticated users cannot access others' carts."""
        url = reverse("cart-detail")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_proceed_to_checkout(self):
        """Ensure authenticated users can proceed to checkout their order."""
        response = self.client.post(self.checkout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_submit_review(self):
        """Ensure authenticated users can submit a product review."""
        review_data = {"rating": 5, "comment": "Great product!"}
        response = self.client.post(self.review_url, data=review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_view_own_order(self):
        """Ensure authenticated users can view their own order details."""
        order = Order.objects.create(user=self.user, total_price=100.00)
        url = reverse("order-detail", args=[order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_view_others_order(self):
        """Ensure authenticated users cannot view others' order details."""
        other_user = CustomUser.objects.create_user(
            username="otheruser", password="password"
        )
        order = Order.objects.create(user=other_user, total_price=100.00)
        url = reverse("order-detail", args=[order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
