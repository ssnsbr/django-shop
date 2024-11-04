from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import (
    Category,
    Product,
    ProductType,
    TypeAttribute,
    ProductAttributeValue,
    ProductMedia,
)
from django.urls import reverse
from attributes.models import Attribute, AttributeOption
from product_variants.models import ProductVariant


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

    # def test_product_available_products(self):
    #     available_products = Product.available_products()
    #     self.assertIn(self.product, available_products)

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
        invalid_image_data = b"invalid image data"
        invalid_image = SimpleUploadedFile(
            "invalid_image.jpg", invalid_image_data, content_type="image/jpeg"
        )
        # invalid_image = BytesIO(b"invalid image data")
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


class ProductTypeAttributeModelTest(TestCase):

    def setUp(self):
        self.product_type = ProductType.objects.create(
            name="Clothing", slug="clothing", description="Clothing description"
        )
        self.attribute = Attribute.objects.create(
            name="Color", description="Product color", attribute_type=Attribute.LOCAL
        )
        self.product_type_attribute = TypeAttribute.objects.create(
            product_type=self.product_type, attribute=self.attribute, is_required=True
        )

    def test_product_type_attribute_creation(self):
        self.assertTrue(isinstance(self.product_type_attribute, TypeAttribute))
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
        self.attribute = Attribute.objects.create(
            name="Color", description="Product color", attribute_type=Attribute.LOCAL
        )
        self.attribute_option = AttributeOption.objects.create(
            attribute=self.attribute, value="Red"
        )
        self.attribute_value = ProductAttributeValue.objects.create(
            product=self.product, attribute=self.attribute, option=self.attribute_option
        )

    def test_product_attribute_value_creation(self):
        self.assertTrue(isinstance(self.attribute_value, ProductAttributeValue))
        self.assertEqual(
            self.attribute_value.__str__(),
            f"{self.product.name} - {self.attribute.name}: {self.attribute_value.option}",
        )


class ProductVariantTest(TestCase):
    def setUp(self):
        # Create necessary objects for the test
        self.product = Product.objects.create(name="Test Product")
        self.attribute_size = Attribute.objects.create(name="size", attribute_type=Attribute.LOCAL)
        self.attribute_color = Attribute.objects.create(name="color", attribute_type=Attribute.LOCAL)

        # Create attribute options
        self.size_option = AttributeOption.objects.create(attribute=self.attribute_size, value="38")
        self.color_option = AttributeOption.objects.create(attribute=self.attribute_color, value="White")

        # Create attribute values
        self.size_value = ProductAttributeValue.objects.create(
            product=self.product, attribute=self.attribute_size, option=self.size_option
        )
        self.color_value = ProductAttributeValue.objects.create(
            product=self.product, attribute=self.attribute_color, option=self.color_option
        )

    def test_unique_variant_creation(self):
        # Create a ProductVariant with the given attributes
        variant1 = ProductVariant.objects.create(product=self.product, name="Variant 1")
        variant1.attributes.add(self.size_value, self.color_value)

        # Try to create a duplicate variant
        variant2 = ProductVariant(product=self.product, name="Variant 2")
        variant2.attributes.add(self.size_value, self.color_value)

        # Check that a ValidationError is raised on save
        with self.assertRaises(ValidationError):
            variant2.save()

    def test_non_duplicate_variant_creation(self):
        # Create a ProductVariant with different attributes to avoid duplication
        variant1 = ProductVariant.objects.create(product=self.product, name="Variant 1")
        variant1.attributes.add(self.size_value, self.color_value)

        # Create a different attribute option and value
        new_color_option = AttributeOption.objects.create(attribute=self.attribute_color, value="Black")
        new_color_value = ProductAttributeValue.objects.create(
            product=self.product, attribute=self.attribute_color, option=new_color_option
        )

        # Create a non-duplicate variant with different color
        variant2 = ProductVariant.objects.create(product=self.product, name="Variant 2")
        variant2.attributes.add(self.size_value, new_color_value)

        # This should not raise an error, so we assert that variant2 is saved successfully
        variant2.save()
        self.assertEqual(ProductVariant.objects.count(), 2)
