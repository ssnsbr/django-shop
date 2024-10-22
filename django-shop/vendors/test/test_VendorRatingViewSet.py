from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Vendor, VendorRating
from faker import Faker

fake = Faker()
User = get_user_model()

vendors_detail_url = "vendors-detail"
vendors_list_url = "vendors-list"
vendors_product_list_url = "vendor-products-list"
vendors_product_detail_url = "vendor-products-detail"
rating_list_url = "vendor-ratings-list"
rating_detail_url = "vendor-ratings-detail"


class VendorRatingViewSetTestCase(APITestCase):
    """Test case for VendorRating viewsets"""

    def setUp(self):
        """Set up necessary user, vendor, and rating"""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.vendoruser = User.objects.create_user(
            username="vendoruser", password="password"
        )

        self.vendor = Vendor.objects.create(
            owner=self.vendoruser,
            store_name=fake.company(),
            store_address=fake.address(),
        )
        self.vendor_rating = VendorRating.objects.create(
            vendor=self.vendor, user=self.user, rating=5, review="Excellent store!"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_vendor_ratings(self):
        """Test listing vendor ratings"""
        response = self.client.get(reverse(rating_list_url, args=[self.vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_vendor_rating(self):
        """Test retrieving a specific vendor rating"""
        response = self.client.get(
            reverse(
                rating_detail_url,
                kwargs={"vendor_pk": self.vendor.id, "pk": self.vendor_rating.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["review"], "Excellent store!")
