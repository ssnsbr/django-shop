from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Product, ProductMedia

from vendor_products.models import VendorListing
from vendors.models import Vendor
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

vendors_detail_url = "vendors-detail"
vendors_list_url = "vendors-list"
vendors_product_list_url = "vendor-products-list"
vendors_product_detail_url = "vendor-products-detail"
rating_list_url = "vendor-ratings-list"
rating_detail_url = "vendor-ratings-detail"


class VendorUserTests(APITestCase):

    def setUp(self):
        # Create vendor user, vendor, and product
        self.vendor_user = CustomUser.objects.create_user(
            username="vendoruser", password="password"
        )
        self.client.login(username="vendoruser", password="password")
        self.vendor = Vendor.objects.create(
            store_name="Test Vendor", owner=self.vendor_user
        )
        self.product_ = Product.objects.create(name="Test Product")
        self.product_media_1 = ProductMedia.objects.create(
            product=self.product_, image="path/to/image.jpg"
        )
        self.product = VendorListing.objects.create(
            product=self.product_,
            price=100.00,
            warehouse_quantity=50,
            vendor=self.vendor,
        )

        self.product_url = reverse(
            vendors_product_detail_url,
            kwargs={"vendor_pk": self.vendor.id, "pk": self.product.id},
        )

    def test_vendor_can_view_own_product_details(self):
        """Ensure vendors can view their own product details."""
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_can_add_and_update_own_product(self):
        """Ensure vendors can add and update their own products."""
        url = reverse(vendors_product_list_url, kwargs={"vendor_pk": self.vendor.id})
        self.product_2 = Product.objects.create(name="Test Product")
        self.product_media_2 = ProductMedia.objects.create(
            product=self.product_2, image="path/to/image.jpg"
        )
        data = {
            "product": self.product_2.id,
            "price": 200.00,
            "warehouse_quantity": 30,
            "vendor": self.vendor.id,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data["id"]

        update_url = reverse(
            vendors_product_detail_url,
            kwargs={"vendor_pk": self.vendor.id, "pk": product_id},
        )
        update_data = {"warehouse_quantity": 60}
        response = self.client.patch(update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_cannot_modify_other_vendors_product(self):
        """Ensure vendors cannot modify products from other vendors."""

        other_vendor = Vendor.objects.create(
            store_name="Other Vendor",
            owner=CustomUser.objects.create_user(
                username="othervendoruser", password="password"
            ),
        )
        tempproduct = Product.objects.create(
            name="Other product",
        )
        self.product_media_2 = ProductMedia.objects.create(
            product=tempproduct, image="path/to/image.jpg"
        )
        other_product = VendorListing.objects.create(
            product=tempproduct,
            price=100.00,
            warehouse_quantity=50,
            vendor=other_vendor,
        )
        url = reverse(
            vendors_product_detail_url,
            kwargs={"vendor_pk": self.vendor.id, "pk": other_product.id},
        )
        data = {"warehouse_quantity": 30}
        response = self.client.patch(url, data)
        print("Should not be able to :", response.status_code, response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
