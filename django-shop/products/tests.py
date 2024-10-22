from django.test import TestCase

from django.core.exceptions import ValidationError
from products.models import (
    Category,
    Product,
    ProductType,
    ProductAttribute,
    ProductTypeAttribute,
    ProductAttributeValue,
    ProductMedia,
)
from django.urls import reverse
from io import BytesIO


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Sportswear",
            slug="sportswear",
            description_text="Description for sportswear",
        )

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), self.category.name)

    def test_category_background_image_alt(self):
        self.category.background_image_alt = "Image Alt Text"
        self.category.save()
        self.assertEqual(self.category.background_image_alt, "Image Alt Text")


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Sportswear",
            slug="sportswear",
            description_text="Sportswear category",
        )
        self.product_type = ProductType.objects.create(
            name="Clothing", slug="clothing", description="Clothing description"
        )
        self.product = Product.objects.create(
            name="Running Shoes",
            description_text="Best shoes for running",
            description_json="{}",
            category=self.category,
            product_type=self.product_type,
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.__str__(), self.product.name)

    def test_product_slug_creation(self):
        self.product.slug = "running-shoes"
        self.product.save()
        self.assertEqual(self.product.slug, "running-shoes")

    def test_product_available_products(self):
        available_products = Product.available_products()
        self.assertIn(self.product, available_products)

    def test_product_get_absolute_url(self):
        self.assertEqual(
            self.product.get_absolute_url(),
            reverse("product_detail", args=[str(self.product.id)]),
        )


class ProductMediaModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Sportswear", slug="sportswear")
        self.product = Product.objects.create(
            name="Running Shoes",
            description_text="Best shoes for running",
            description_json="{}",
            category=self.category,
        )

    def test_product_media_creation(self):
        media = ProductMedia.objects.create(
            product=self.product,
            alt="Running Shoes Image",
            external_url="http://example.com",
        )
        self.assertTrue(isinstance(media, ProductMedia))
        self.assertEqual(media.alt, "Running Shoes Image")

    def test_invalid_image(self):
        invalid_image = BytesIO(b"invalid image data")
        with self.assertRaises(ValidationError):
            ProductMedia.objects.create(product=self.product, image=invalid_image)


class ProductTypeModelTest(TestCase):

    def setUp(self):
        self.product_type = ProductType.objects.create(
            name="Clothing", slug="clothing", description="Clothing description"
        )

    def test_product_type_creation(self):
        self.assertTrue(isinstance(self.product_type, ProductType))
        self.assertEqual(self.product_type.__str__(), self.product_type.name)


class ProductAttributeModelTest(TestCase):

    def setUp(self):
        self.attribute = ProductAttribute.objects.create(
            name="Color", description="Product color"
        )

    def test_product_attribute_creation(self):
        self.assertTrue(isinstance(self.attribute, ProductAttribute))
        self.assertEqual(self.attribute.__str__(), self.attribute.name)


class ProductTypeAttributeModelTest(TestCase):

    def setUp(self):
        self.product_type = ProductType.objects.create(
            name="Clothing", slug="clothing", description="Clothing description"
        )
        self.attribute = ProductAttribute.objects.create(
            name="Color", description="Product color"
        )
        self.product_type_attribute = ProductTypeAttribute.objects.create(
            product_type=self.product_type, attribute=self.attribute, is_required=True
        )

    def test_product_type_attribute_creation(self):
        self.assertTrue(isinstance(self.product_type_attribute, ProductTypeAttribute))
        self.assertEqual(
            self.product_type_attribute.__str__(),
            f"{self.product_type.name} - {self.attribute.name}",
        )


class ProductAttributeValueModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Sportswear", slug="sportswear")
        self.product_type = ProductType.objects.create(
            name="Clothing", slug="clothing", description="Clothing description"
        )
        self.product = Product.objects.create(
            name="Running Shoes",
            description_text="Best shoes for running",
            description_json="{}",
            category=self.category,
            product_type=self.product_type,
        )
        self.attribute = ProductAttribute.objects.create(
            name="Color", description="Product color"
        )
        self.attribute_value = ProductAttributeValue.objects.create(
            product=self.product, attribute=self.attribute, value="Red"
        )

    def test_product_attribute_value_creation(self):
        self.assertTrue(isinstance(self.attribute_value, ProductAttributeValue))
        self.assertEqual(
            self.attribute_value.__str__(),
            f"{self.product.name} - {self.attribute.name}: {self.attribute_value.value}",
        )
