from django.contrib.auth import get_user_model

from products.models import Product, ProductMedia
from vendor_products.models import VendorListing
from vendors.models import Vendor

from faker import Faker
from faker.providers import company

fake = Faker("en-PH")
# TODO : Pull request to https://github.com/joke2k/faker for fa-IR and random_company_product
fake.add_provider(company)


class TestUtils:
    @staticmethod
    def create_user():
        return get_user_model().objects.create_user(
            username=fake.user_name(), password=fake.password()
        )

    @staticmethod
    def create_vendor(user=None):
        if user is None:
            user = TestUtils.create_user()
        return Vendor.objects.create(store_name=fake.company(), owner=user)

    @staticmethod
    def create_product():
        product = Product.objects.create(name=fake.random_company_product())
        product_media_list = []
        for i in range(fake.random_int(min=1, max=6)):
            product_media = ProductMedia.objects.create(
                product=product,
                image="path/to/image_" + str(fake.random_number(5)) + ".jpg",
            )
            product_media_list.append(product_media)
        return product

    @staticmethod
    def create_vendor_product(vendor=None, product=None):

        if vendor is None:
            vendor = TestUtils.create_vendor()
        if product is None:
            product = TestUtils.create_product()
        return VendorListing.objects.create(
            product=product,
            price=fake.random_number(3) * 1000,
            warehouse_quantity=fake.random_number(2),
            vendor=vendor,
        )
