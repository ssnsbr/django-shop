from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vendor_products.models import VendorListing
from vendors.models import Vendor
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class AdminUserTests(APITestCase):

    def setUp(self):
        # Create admin user, vendor, and product
        self.admin_user = CustomUser.objects.create_superuser(username="admin", password="adminpassword")
        self.client.login(username="admin", password="adminpassword")
        self.vendoruser = get_user_model().objects.create_user(
            username="testuservendor", password="password"
        )
        self.vendor = Vendor.objects.create(owner=self.vendoruser, store_name="Test Vendor")

        self.product = VendorListing.objects.create(
            name="Test Product", price=100.00, warehouse_quantity=50, vendor=self.vendor
        )
        self.product_url = reverse('vendorproduct-detail', args=[self.product.id])
        self.vendor_url = reverse('vendor-detail', args=[self.vendor.id])

    def test_admin_can_view_and_update_all_products(self):
        """Ensure admin users can view and update all product details."""
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        update_data = {"warehouse_quantity": 100}
        response = self.client.patch(self.product_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_view_and_edit_all_vendor_details(self):
        """Ensure admin users can view and edit all vendor details."""
        response = self.client.get(self.vendor_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        update_data = {"phone": "1234567890"}
        response = self.client.patch(self.vendor_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_view_and_manage_all_orders_and_payments(self):
        """Ensure admin users can view and manage all orders and payments."""
        # Implement order and payment models and endpoints as needed
        pass

    def test_admin_can_manage_user_accounts(self):
        """Ensure admin users can manage user accounts, including authentication, permissions, and profiles."""
        # Implement user account management as needed
        pass
