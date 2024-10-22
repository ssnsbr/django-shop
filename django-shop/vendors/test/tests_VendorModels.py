from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Vendor, VendorProduct
from products.models import Product
from faker import Faker

fake = Faker()
User = get_user_model()

vendors_detail_url = "vendors-detail"
vendors_list_url = "vendors-list"
vendors_product_list_url = "vendor-products-list"
vendors_product_detail_url = "vendor-products-detail"
rating_list_url = "vendor-ratings-list"
rating_detail_url = "vendor-ratings-detail"


# Vendor model tests
class VendorModelTestCase(TestCase):
    """Test case for the Vendor model"""

    def setUp(self):
        """Create a user and a vendor for testing"""
        self.user = User.objects.create_user(username="vendoruser", password="password")
        self.vendor = Vendor.objects.create(
            owner=self.user,
            store_name=fake.company(),
            store_address=fake.address(),
            store_bio=fake.text(),
            contact_number=fake.phone_number(),
        )

    def test_vendor_creation(self):
        """Test that a vendor can be successfully created"""
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(self.vendor.owner, self.user)

    def test_str_representation(self):
        """Test the string representation of the Vendor"""
        self.assertEqual(str(self.vendor), self.vendor.store_name)

    def test_get_vendor_products(self):
        """Test that the vendor can retrieve related products"""
        product = Product.objects.create(name="Test Product")
        VendorProduct.objects.create(
            vendor=self.vendor, product=product, price=10.00, warehouse_quantity=100
        )
        products = self.vendor.get_vendor_products()
        self.assertEqual(products.count(), 1)

    # Add test to ensure vendor cannot be created without required fields
    def test_vendor_creation_invalid_data(self):
        """Test that creating a vendor with missing required fields fails"""
        with self.assertRaises(Exception):  # Assuming Django will raise an error
            Vendor.objects.create(
                owner=self.user,
                store_name=None,  # Missing required field
                store_address=fake.address(),
                contact_number=fake.phone_number(),
            )
