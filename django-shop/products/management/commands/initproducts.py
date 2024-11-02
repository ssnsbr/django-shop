from os import pardir, path
import random
from definitions import ROOT_DIR
__author__ = 'admin@email.com'

import glob
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductType, ProductAttribute, ProductTypeAttribute, ProductAttributeValue, ProductMedia, ProductAttributeOption, ProductVariant
from vendors.models import Vendor
from vendor_products.models import VendorListing
from tests.test_common import TestUtils
from faker import Faker
fake = Faker("fa-IR")
category_names = ["لباس", "مولتی مدیا"]
category_slugs = ["cloth", "multimedia"]
clothـsub_category_names = ["محافظ", "کفش"]
clothـsub_category_slugs = ["protective-gear", "shoe"]
multimediaـsub_category_names = ["دی وی دی", "کتاب"]
multimediaـsub_category_slugs = ["dvd", "books"]
#
product_types = ["تی شرت", "کفش", "کتاب", "دی وی دی"]
product_types_slugs = ["t-shirt", "shoe", "book", "dvd"]
# attributes and att_values
materia_att = {"material": ["Cotton", "Polyester", "Blend", "Nylon"], "local": False}
color_att = {"color": ["White", "Black"], "local": True}  # , "Blue", "Red", "Green", "Yellow"
shoe_size_att = {"size": [38, 39], "local": True}  # , 40, 41, 42, 43
t_shirt_size_att = {"size": ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"], "local": True}
t_shirt_sleeve_att = {"sleeve": ["Short", "Long", "Half-length"], "local": False}
brand_att = {"brand": ["Adidas", "Nike", "Puma", "Fila", "Levi's"], "local": False}
publisher_att = {"publisher": ["Publisher1", "Publisher2"], "local": False}
# types and attributes
types_and_attributes = {"t-shirt": [color_att, t_shirt_size_att, t_shirt_sleeve_att, brand_att, materia_att],
                        "shoe": [color_att, brand_att, materia_att, shoe_size_att],
                        "book": [publisher_att],
                        "dvd": [publisher_att]}


class Command(BaseCommand):
    help = "Populate the database with fake products and related data"

    def populate_categories(self):
        self.categories = []
        for i, cat_name in enumerate(category_names):
            self.categories.append(
                Category.objects.create(
                    name=cat_name, description_text=cat_name, slug=category_slugs[i]
                )
            )
        for i, cat_name in enumerate(clothـsub_category_names):
            self.categories.append(
                Category.objects.create(
                    parent=self.categories[0], name=cat_name, description_text=cat_name, slug=clothـsub_category_slugs[i]
                )
            )
        for i, cat_name in enumerate(multimediaـsub_category_names):
            self.categories.append(
                Category.objects.create(
                    parent=self.categories[1], name=cat_name, description_text=cat_name, slug=multimediaـsub_category_slugs[i]
                )
            )
        self.stdout.write(
            self.style.SUCCESS("Successfully added Categories to the database.")
        )

    def populate_users(self):
        self.customer_users = [
            get_user_model().objects.create_user(
                username="customer_1",
                email="customer_1@email.com",
                password="testpass123",
            ),
            get_user_model().objects.create_user(
                username="customer_2",
                email="customer_2@email.com",
                password="testpass123",
            ),
            get_user_model().objects.create_user(
                username="customer_3",
                email="customer_3@email.com",
                password="testpass123",
            ),
            TestUtils.create_user(),
            TestUtils.create_user(),
            TestUtils.create_user()
        ]
        self.stdout.write(
            self.style.SUCCESS("Successfully added Users to the database.")
        )

    def populate_vendors(self):
        self.vendor_users = [
            get_user_model().objects.create_user(
                username="vendor1", email="vendor1@email.com", password="testpass123"
            ),
            get_user_model().objects.create_user(
                username="vendor2", email="vendor2@email.com", password="testpass123"
            ),
            get_user_model().objects.create_user(
                username="vendor3", email="vendor3@email.com", password="testpass123"
            ),
            TestUtils.create_user(),
            TestUtils.create_user()
        ]
        self.stdout.write(
            self.style.SUCCESS("Successfully add Vendor Users to the database.")
        )
        vendor_names = [
            "فروشگاه ورزشی الف",
            "فروشگاه ورزشی ب",
            "فروشگاه ورزشی ج",
        ]
        vendor_bios = [
            "ما فروشگاه ورزشی الف هستیم",
            "ما فروشگاه ورزشی ب هستیم",
            "ما فروشگاه ورزشی ج هستیم",
        ]
        self.vendors = []
        for i, name in enumerate(vendor_names):
            vendor = Vendor.objects.create(
                owner=self.vendor_users[i],
                store_name=name,
                store_address=fake.text(),
                store_bio=vendor_bios[i],
                contact_number=fake.random_int(min=11111, max=31111),
            )
            self.vendors.append(vendor)
        self.vendors.append(TestUtils.create_vendor())
        self.vendors.append(TestUtils.create_vendor())

        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with fake vendors")
        )

    def populate_types(self):
        self.product_types_list = []
        for i, type_name in enumerate(product_types):
            self.product_types_list.append(
                ProductType.objects.create(
                    name=type_name, description=type_name, slug=product_types_slugs[i]
                )
            )
        self.stdout.write(
            self.style.SUCCESS("Successfully added Types to the database.")
        )

    def populate_products_types_attributes(self):
        for type, att_dic_list in types_and_attributes.items():
            for att_dic in att_dic_list:  # {"size": [38, 39, 40, 41, 42, 43]}
                k = list(att_dic.keys())[0]  # "size"
                t = ProductType.objects.get(slug=type)
                ـProductAttribute = ProductAttribute.objects.create(
                    name=k,
                    description=k,
                    attribute_type=ProductAttribute.LOCAL if att_dic["local"] else ProductAttribute.GLOBAL,
                )
                for v in att_dic[k]:  # [38, 39, 40, 41, 42, 43]
                    ProductAttributeOption.objects.create(
                        value=v,
                        attribute=ـProductAttribute,
                    )
                ProductTypeAttribute.objects.create(
                    attribute=ـProductAttribute,
                    product_type=t,
                    is_required=False
                )
        self.stdout.write(
            self.style.SUCCESS("Successfully added ProductAttribute/Options/Types to the database.")
        )

    def populate_products(self):
        sample_product = {"name": "کفش نایک آبی",
                          "product_type": "shoe",
                          "description": "عالی!",
                          "slug": "nike-blue-209999",
                          "category": "shoe"
                          }
        product_type = ProductType.objects.get(slug=sample_product["product_type"])

        selected_images = fake.random_elements(
            elements=self.images_list, length=random.randint(1, 5), unique=True
        )

        product = Product.objects.create(
            name=sample_product["name"],
            category=Category.objects.get(slug=sample_product["category"]),
            description_text=sample_product["description"],
            slug=sample_product["slug"],
            product_type=product_type,
        )
        for i in selected_images:
            ProductMedia.objects.create(
                product=product,
                image=i,
            )
        self.stdout.write(
            self.style.SUCCESS("Successfully added Products to the database.")
        )

    def populate_product_variants(self):
        _product_obj = random.choice(Product.objects.all())
        # _product_variant_obj = _product_obj.variants.all()
        _product_variant_obj = ProductVariant.objects.create(product=_product_obj)
        # _obj_atts = _product_obj.product_type.attributes.all()
        _obj_atts = ProductTypeAttribute.objects.filter(product_type=_product_obj.product_type)
        for sample_att in (_obj_atts):  # random.sample(list(_obj_atts), random.randint(0, len(_obj_atts))):
            # sample_att = sample_att.attribute
            # print(sample_att.__class__)
            if sample_att.attribute.attribute_type == ProductAttribute.LOCAL:
                _obj_atts_options = ProductAttributeOption.objects.filter(attribute=sample_att.attribute)
                _product_variant_obj.attributes.add(
                    ProductAttributeValue.objects.create(product=_product_obj,
                                                         attribute=sample_att.attribute,
                                                         option=random.choice(_obj_atts_options)))

        VendorListing.objects.create(
            product=_product_obj,
            product_variant=_product_variant_obj,
            vendor=random.choice(Vendor.objects.all()),
            warehouse_quantity=random.randint(5, 50),
            price=random.randint(5, 500) * 1000)

    def handle(self, *args, **options):
        # print(path.join(path.abspath(path.join(ROOT_DIR, pardir)), "fakephotos\\saloerphotos\\saloerplaceholders\\*.png"))
        images_path = path.abspath(path.join(ROOT_DIR, pardir))
        self.images_list = glob.glob(path.join(images_path, "fakephotos\\saloerplaceholders\\*.png"))
        self.images_list = [x[len(images_path):] for x in self.images_list]
        # print(self.images_list)

        # Category.objects.all().delete()
        # self.populate_categories()

        # ProductType.objects.all().delete()
        # self.populate_types()

        # get_user_model().objects.all().delete()
        # self.populate_users()

        # Vendor.objects.all().delete()
        # self.populate_vendors()

        ProductAttribute.objects.all().delete()
        ProductAttributeOption.objects.all().delete()
        ProductTypeAttribute.objects.all().delete()
        self.populate_products_types_attributes()

        Product.objects.all().delete()
        self.populate_products()

        VendorListing.objects.all().delete()
        ProductVariant.objects.all().delete()
        for i in range(10):
            self.populate_product_variants()
