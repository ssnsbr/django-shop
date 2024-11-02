from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from vendors.models import Vendor
from products.models import Product, ProductMedia
from vendor_products.models import VendorListing
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
User = get_user_model()


class SearchViewTestCase(APITestCase):
    def setUp(self):
        """Set up necessary data for tests"""
        # Create users
        self.vendor_user = User.objects.create_user(username="vendor_user", password="password")
        self.other_user = User.objects.create_user(username="other_user", password="password")

        # Create vendors
        self.vendor1 = Vendor.objects.create(
            owner=self.vendor_user,
            store_name="TechStore",
            store_address=fake.address(),
            store_bio="Best tech products",
            contact_number=fake.phone_number(),
        )
        self.vendor2 = Vendor.objects.create(
            owner=self.vendor_user,
            store_name="PhoneHub",
            store_address=fake.address(),
            store_bio="Best phones in town",
            contact_number=fake.phone_number(),
        )

        # Create products
        self.product1 = Product.objects.create(name="iPhone", description="Latest Apple iPhone")
        self.product2 = Product.objects.create(name="Samsung Galaxy", description="Latest Samsung phone")
        self.product_media_1 = ProductMedia.objects.create(
            product=self.product1,
            image="path/to/image.jpg"
        )
        self.product_media_2 = ProductMedia.objects.create(
            product=self.product2,
            image="path/to/image.jpg"
        )
        # Link products to vendors
        VendorListing.objects.create(vendor=self.vendor1, product=self.product1, price="999.99", warehouse_quantity=10)
        VendorListing.objects.create(vendor=self.vendor2, product=self.product2, price="799.99", warehouse_quantity=20)

        self.client = APIClient()

    def test_search_for_product(self):
        """Test search functionality for product names"""
        url = reverse('search') + "?q=iPhone"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['products']), 1)
        self.assertEqual(response.data['products'][0]['name'], "iPhone")

    def test_search_for_vendor(self):
        """Test search functionality for vendor store names"""
        url = reverse('search') + "?q=TechStore"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['vendors']), 1)
        self.assertEqual(response.data['vendors'][0]['store_name'], "TechStore")

    def test_search_for_vendor_and_product(self):
        """Test search functionality for both vendor and product in the same query"""
        url = reverse('search') + "?q=phone"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # There should be results for both products and vendors
        self.assertGreaterEqual(len(response.data['products']), 1)
        self.assertGreaterEqual(len(response.data['vendors']), 1)

    def test_empty_search_query(self):
        """Test search with no query parameter"""
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No search query provided.", response.data['error'])

    def test_search_for_nonexistent_data(self):
        """Test search that should return no results"""
        url = reverse('search') + "?q=NonExistentProduct"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['products']), 0)
        self.assertEqual(len(response.data['vendors']), 0)
