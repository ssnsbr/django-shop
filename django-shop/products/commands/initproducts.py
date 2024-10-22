__author__ = 'admin@email.com'

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category

category_names = ["لباس", "مولتی مدیا"]
category_slugs = ["cloth", "multimedia"]
clothـsub_category_names = ["محافظ", "کفش"]
clothـsub_category_slugs = ["protective-gear", "shoe"]

product_types_and_attributes = {"t-shirt": [{"size": ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"]}, {"color": ["red", "blue", "green", "yellow"]}, "material", "brand", "sleeve"], "shoe": ["size", "color", "material", "brand", "type", "sole_type"], "book": ["publisher"]}


class Command(BaseCommand):
    help = "Populate the database with fake products and related data"

    def populate_categories(self):
        self.categories = []
        for i, cat_name in enumerate(category_names):
            self.categories.append(
                Category.objects.create(
                    name=cat_name, description=cat_name, slug=category_slugs[i]
                )
            )
        for i, cat_name in enumerate(clothـsub_category_names):
            self.categories.append(
                Category.objects.create(
                    parent=self.categories[0], name=cat_name, description=cat_name, slug=clothـsub_category_slugs[i]
                )
            )

    def handle(self, *args, **options):
        if get_user_model().objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = 'admin'
                print('Creating account for %s (%s)' % (username, email))
                admin = get_user_model().objects.create_superuser(email=email, username=username, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
