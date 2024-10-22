from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vendors.models import Vendor
from products.models import Product
from django.contrib.auth import get_user_model


class UnauthenticatedUserTests(APITestCase):

    def setUp(self):
        # Create a vendor and product for testing
        self.vendoruser = get_user_model().objects.create_user(
            username="testuservendor", password="password"
        )

        self.vendor = Vendor.objects.create(owner=self.vendoruser, store_name="Test Vendor")

        self.vendor = Vendor.objects.create(store_name="Test Vendor")
        self.product = Product.objects.create(name="Test Product", price=50.00)

    def test_unauthenticated_user_can_view_product_details(self):
        """Ensure unauthenticated users can view product details."""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_can_view_vendor_details(self):
        """Ensure unauthenticated users can view vendor details."""
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_view_order(self):
        """Ensure unauthenticated users cannot view any order details or payment information."""
        url = reverse('order-detail', args=[1])  # Replace with a valid order ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_view_vendor_personal_info(self):
        """Ensure unauthenticated users cannot view vendor's personal information."""
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertNotIn('phone', response.data)

    def test_unauthenticated_user_cannot_add_to_cart(self):
        """Ensure unauthenticated users cannot add items to the cart."""
        url = reverse('cart-add', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_access_cart(self):
        """Ensure unauthenticated users cannot access the cart."""
        url = reverse('cart-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_checkout(self):
        """Ensure unauthenticated users cannot proceed to checkout."""
        url = reverse('checkout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_submit_review(self):
        """Ensure unauthenticated users cannot submit a product review."""
        url = reverse('product-review', args=[self.product.id])
        review_data = {
            "rating": 5,
            "comment": "Great product!"
        }
        response = self.client.post(url, data=review_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_view_vendor_warehouse_quantity(self):
        """Ensure unauthenticated users cannot view vendor's warehouse quantity."""
        url = reverse('vendorproduct-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertNotIn('warehouse_quantity', response.data)
