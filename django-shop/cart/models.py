import uuid
from django.db import models

from django.contrib.auth import get_user_model

from vendor_products.models import VendorListing


# Cart model to handle user's shopping cart
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def __len__(self):
        """
        count all items in the cart.
        :return:
        """
        all_cart_items = self.items.all()
        return sum(item.quantity for item in all_cart_items)

    def get_items(self):
        return self.items.all()

    def get_total_price(self):
        all_cart_items = self.items.all()
        return sum(item.vendor_product.price * item.quantity for item in all_cart_items)

    def clear(self):
        # remove cart(table) from session
        pass


# CartItem model to handle individual items within a cart
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    vendor_product = models.ForeignKey(
        VendorListing, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CartItem: {self.vendor_product.product.name} (x{self.quantity}) in cart of {self.cart.user.username}"
