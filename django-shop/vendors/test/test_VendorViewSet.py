from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Vendor
from faker import Faker

fake = Faker()
User = get_user_model()

vendors_detail_url = "vendors-detail"
vendors_list_url = "vendors-list"
vendors_product_list_url = "vendor-products-list"
vendors_product_detail_url = "vendor-products-detail"
rating_list_url = "vendor-ratings-list"
rating_detail_url = "vendor-ratings-detail"


# Vendor viewset tests
class VendorViewSetTestCase(APITestCase):
    """Test case for Vendor viewsets"""

    def setUp(self):
        """Create a user, vendor, and client"""
        self.client = APIClient()
        self.user = User.objects.create_user(username="vendoruser", password="password")
        self.client.force_authenticate(user=self.user)
        self.vendor = Vendor.objects.create(
            owner=self.user,
            store_name=fake.company(),
            store_address=fake.address(),
            store_bio=fake.text(),
            contact_number=fake.phone_number(),
        )

    def test_list_vendors(self):
        """Test that we can list vendors"""
        response = self.client.get(reverse(vendors_list_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_vendor(self):
        """Test that we can retrieve a specific vendor"""
        response = self.client.get(reverse(vendors_detail_url, args=[self.vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_name"], self.vendor.store_name)

    def test_create_vendor(self):
        """Test that we can create a new vendor!"""
        payload = {
            "store_name": "New Store",
            "store_address": fake.address(),
            "store_bio": fake.text(),
            "contact_number": fake.phone_number(),
            "owner": self.user.id,
        }
        response = self.client.post(reverse(vendors_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)
        self.assertEqual(Vendor.objects.latest("id").store_name, "New Store")

    # Add a test for creating a vendor without authentication
    def test_create_vendor_unauthenticated(self):
        """Test that creating a vendor without authentication fails"""
        self.client.logout()
        payload = {
            "store_name": "Unauthorized Store",
            "store_address": fake.address(),
            "store_bio": fake.text(),
            "contact_number": fake.phone_number(),
            "owner": self.user.id,
        }
        response = self.client.post(reverse(vendors_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_vendor(self):
        """Test that we can update a vendor"""
        payload = {"store_name": "Updated Store Name"}
        response = self.client.patch(
            reverse(vendors_detail_url, args=[self.vendor.id]), payload
        )
        print(response.content)
        self.vendor.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.vendor.store_name, "Updated Store Name")

    # Add a negative test for deleting a non-existent vendor
    def test_delete_nonexistent_vendor(self):
        """Test deleting a non-existent vendor returns 404"""
        response = self.client.delete(reverse(vendors_detail_url, args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
