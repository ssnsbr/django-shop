from django.test import TestCase  # noqa
from .models import Attribute
# Create your tests here.


class AttributeModelTest(TestCase):

    def setUp(self):
        self.attribute = Attribute.objects.create(
            name="Color", description="Product color", attribute_type=Attribute.LOCAL
        )

    def test_product_attribute_creation(self):
        self.assertTrue(isinstance(self.attribute, Attribute))
        self.assertEqual(self.attribute.__str__(), self.attribute.name)
