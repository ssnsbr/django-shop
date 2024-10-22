from rest_framework.test import APITestCase
from tests.test_common import TestUtils
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

vendors_detail_url = "vendors-detail"
vendors_list_url = "vendors-list"
vendors_product_list_url = "vendor-products-list"
vendors_product_detail_url = "vendor-products-detail"
rating_list_url = "vendor-ratings-list"
rating_detail_url = "vendor-ratings-detail"


class UserBuyingTests(APITestCase):

    def setUp(self):
        print("setUp")
        self.vendor = TestUtils.create_vendor()
        self.vendor_user = self.vendor.owner
        self.client.login(
            username=self.vendor_user.username, password=self.vendor_user.password
        )
        self.vendor = TestUtils.create_vendor(self.vendor_user)
        self.product = TestUtils.create_product()
        self.vendor_product = TestUtils.create_vendor_product(vendor=self.vendor, product=self.product)

    def test_user_add_to_cart(self):
        pass

    def test_user_make_order_from_cart(self):
        pass

    def test_user_finilize_order(self):
        pass

    def test_user_pay_order(self):
        pass

    def test_user_payment_history(self):
        pass

    def test_user_track_ongoing_order(self):
        pass

    def test_vendors_get_order_details(self):
        pass

    def test_vendors_update_order(self):
        pass

    def test_vendor_cancel_order(self):
        pass

    def test_user_cancel_order(self):
        pass

    def test_vendors_balance(self):
        pass
