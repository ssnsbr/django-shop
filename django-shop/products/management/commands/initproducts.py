from os import pardir, path
import random

from django.db import Error
from definitions import ROOT_DIR
__author__ = 'admin@email.com'

import glob
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Attribute, AttributeOption, AttributeValue, Category, Product, ProductAttributeValue, ProductType, TypeAttribute, ProductMedia
from vendors.models import Vendor
from product_variants.models import ProductVariant, VariantAttributeValue
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
materia_att = {"material": ["Cotton", "Polyester", "Blend", "Nylon"], "type": "variant", "required": True}
color_att = {"color": ["White", "Black", "Blue"], "type": "variant", "required": True}  # , "Blue", "Red", "Green", "Yellow"
shoe_size_att = {"size": [38, 39], "type": "variant", "required": True}  # , 40, 41, 42, 43
t_shirt_size_att = {"size": ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"], "type": "variant", "required": True}
t_shirt_sleeve_att = {"sleeve": ["Short", "Long", "Half-length"], "type": "variant", "required": True}
brand_att = {"brand": ["Adidas", "Nike", "Puma", "Fila", "Levi's"], "type": "product", "required": True}
publisher_att = {"publisher": ["Publisher1", "Publisher2"], "type": "product", "required": True}
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
                _required = att_dic["required"]
                attribute_type = TypeAttribute.VARIANT_ATTRIBUTE if att_dic["type"] == "variant" else TypeAttribute.PRODUCT_ATTRIBUTE
                ـProductAttribute = Attribute.objects.create(
                    name=k,
                    description=k,
                )
                for v in att_dic[k]:  # [38, 39, 40, 41, 42, 43]
                    AttributeOption.objects.create(
                        value=v,
                        attribute=ـProductAttribute,
                    )
                TypeAttribute.objects.create(
                    attribute=ـProductAttribute,
                    product_type=t,
                    is_required=_required,
                    attribute_type=attribute_type
                )
        self.stdout.write(
            self.style.SUCCESS("Successfully added ProductAttribute/Options/Types to the database.")
        )

    def populate_products(self, sample_product):

        _product_type = ProductType.objects.get(slug=sample_product["product_type"])
        print("product_type:", _product_type)
        selected_images = fake.random_elements(
            elements=self.images_list, length=random.randint(1, 5), unique=True
        )

        product = Product.objects.create(
            name=sample_product["name"],
            category=Category.objects.get(slug=sample_product["category"]),
            description_text=sample_product["description"],
            slug=sample_product["slug"],
            product_type=_product_type,
            approved=True,
        )
        product_atts = TypeAttribute.objects.filter(product_type=_product_type)
        for k, v in sample_product["attributes"].items():
            brand_att = product_atts.filter(attribute__name=k).first()
            print("brand_att:", brand_att)
            obj_atts_options = AttributeOption.objects.filter(attribute=brand_att.attribute, value=v).first()
            ProductAttributeValue.objects.create(product=product, attribute=brand_att.attribute,
                                                 option=obj_atts_options)

        for i in selected_images:
            ProductMedia.objects.create(
                product=product,
                image=i,
            )
        self.stdout.write(
            self.style.SUCCESS("Successfully added Products to the database.")
        )

    def populate_product_variants(self, slug, variants):
        _product_obj = Product.objects.get(slug=slug)
        product_atts = TypeAttribute.objects.filter(product_type=_product_obj.product_type)

        for variant in variants:
            for k, v in variant.items():  # size , 39
                brand_att = product_atts.filter(attribute__name=k).first()
                obj_atts_options = AttributeOption.objects.filter(attribute=brand_att.attribute, value=v).first()
                VariantAttributeValue.objects.create(variant=_product_variant_obj, attribute=brand_att.attribute,
                                                     option=obj_atts_options)
            _product_variant_obj = ProductVariant.objects.create(product=_product_obj)

        VendorListing.objects.create(
            product=_product_obj,
            product_variant=_product_variant_obj,
            vendor=random.choice(Vendor.objects.all()),
            warehouse_quantity=random.randint(5, 50),
            price=random.randint(5, 500) * 1000)

    def populate_product_variants2(self, slug, variants):
        _product_obj = Product.objects.get(slug=slug)
        product_atts = TypeAttribute.objects.filter(product_type=_product_obj.product_type)
        att_to_add_to_variant = []
        for variant in variants:
            for k, v in variant.items():  # size , 39
                brand_att = product_atts.filter(attribute__name=k).first()
                obj_atts_options = AttributeOption.objects.filter(attribute=brand_att.attribute, value=v).first()
                # try:
                att_to_add_to_variant.append(AttributeValue.objects.get_or_create(attribute=brand_att.attribute,
                                                                                  option=obj_atts_options))
                # except Error as e:
                #     print(e)
        print("Making ProductVariant:")
        _product_variant_obj = ProductVariant.objects.create(product=_product_obj)
        print("Adding Attributes ProductVariant:", att_to_add_to_variant)

        _product_variant_obj.attributes.set(av[0] for av in att_to_add_to_variant)
        VendorListing.objects.create(
            product=_product_obj,
            product_variant=_product_variant_obj,
            vendor=random.choice(Vendor.objects.all()),
            warehouse_quantity=random.randint(5, 50),
            price=random.randint(5, 500) * 1000)
        # except Error as e:
        #     print(e)
    # def populate_product_variants_2(self):
    #     try:
    #         shoe_product = random.choice(Product.objects.all())
    #         shoe_variant = ProductVariant.objects.create(product=shoe_product)
    #         product_type = shoe_product.product_type
    #         product_attributes = product_type.attributes.all()
    #         # _obj_atts = _product_obj.product_type.attributes.all()
    #         # _obj_atts = TypeAttribute.objects.filter(product_type=_product_obj.product_type)
    #         color_att = _obj_atts.filter(name="color")
    #         size_att = _obj_atts.filter(name="size")
    #         for sample_att in (product_attributes):  # random.sample(list(_obj_atts), random.randint(0, len(_obj_atts))):
    #             if sample_att.attribute_type == Attribute.VARIANT_ATTRIBUTE:
    #                 # sample_att = sample_att.attribute
    #                 # print(sample_att.__class__)
    #             if sample_att.attribute.attribute_type == Attribute.VARIANT_ATTRIBUTE:
    #                 _obj_atts_options = AttributeOption.objects.filter(attribute=sample_att.attribute)
    #                 VariantAttributeValue.objects.create(variant=_product_variant_obj, attribute=sample_att.attribute,
    #                                                      option=random.choice(_obj_atts_options))

    #         VendorListing.objects.create(
    #             product=_product_obj,
    #             product_variant=_product_variant_obj,
    #             vendor=random.choice(Vendor.objects.all()),
    #             warehouse_quantity=random.randint(5, 50),
    #             price=random.randint(5, 500) * 1000)
    #     except Exception as e:
    #         print(e)

    def handle(self, *args, **options):
        # print(path.join(path.abspath(path.join(ROOT_DIR, pardir)), "fakephotos\\saloerphotos\\saloerplaceholders\\*.png"))
        images_path = path.abspath(path.join(ROOT_DIR, pardir))
        self.images_list = glob.glob(path.join(images_path, "fakephotos\\saloerplaceholders\\*.png"))
        self.images_list = [x[len(images_path):] for x in self.images_list]
        # print(self.images_list)

        Category.objects.all().delete()
        self.populate_categories()

        ProductType.objects.all().delete()
        self.populate_types()

        get_user_model().objects.all().delete()
        self.populate_users()

        Vendor.objects.all().delete()
        self.populate_vendors()
        AttributeValue.objects.all().delete()
        Attribute.objects.all().delete()
        AttributeOption.objects.all().delete()
        TypeAttribute.objects.all().delete()
        self.populate_products_types_attributes()

        Product.objects.all().delete()
        self.populate_products(sample_product={"name": "کفش نایک آبی",
                                               "product_type": "shoe",
                                               "description": "عالی!",
                                               "slug": "nike-blue-209999",
                                               "category": "shoe",
                                               "attributes": {"brand": "Nike", "color": "Blue", "material": "Cotton"}
                                               })

        self.populate_products(sample_product={"name": "کفش آدیداس 2099",
                                               "product_type": "shoe",
                                               "description": "عالی!",
                                               "slug": "adidas-2099",
                                               "category": "shoe",
                                               "attributes": {"brand": "Adidas", "material": "Cotton"}
                                               })

        VendorListing.objects.all().delete()
        ProductVariant.objects.all().delete()
        # for i in range(10):
        #     self.populate_product_variants()
        self.populate_product_variants2("adidas-2099", [{"color": "Blue", "size": "38"},
                                                        {"color": "Blue", "size": "39"},
                                                        {"color": "Black", "size": "38"}])
        self.populate_product_variants2("nike-blue-209999", [{"size": "38"},
                                                             {"size": "39"},
                                                             {"size": "39"}])
