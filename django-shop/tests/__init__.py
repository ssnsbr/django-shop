from .test_admin_users  import *
from .test_authenticated_users  import *
from .test_unauthenticated_user  import *
from .test_vendor_users  import *
from .test_user_buying_process import  *

# Unauthenticated Users:
# Ensure unauthenticated users can view product details.
# Ensure unauthenticated users can view vendor details.
# Ensure unauthenticated users cannot view any order details or payment information.
# Ensure unauthenticated users cannot view vendor's personal information.
# Ensure unauthenticated users cannot add items to the cart.
# Ensure unauthenticated users cannot access the cart.
# Ensure unauthenticated users cannot proceed to checkout.
# Ensure unauthenticated users cannot submit a product review.
# Ensure unauthenticated users cannot view vendor's warehouse quantity.
# Authenticated Users:
# Ensure authenticated users can view product details.
# Ensure authenticated users can view vendor details.
# Ensure authenticated users can view vendor's warehouse quantity.
# Ensure authenticated users can view vendor's personal information.
# Ensure authenticated users can add items to their own cart and cannot access others' carts.
# Ensure authenticated users can proceed to checkout their order.
# Ensure authenticated users can submit a product review.
# Ensure authenticated users can view their own order details, payment information, and profile but cannot see others' orders or profiles.
# Vendors:
# Ensure vendors can view their own product details and update them.
# Ensure vendors can add and update their own products but cannot modify products added by other vendors.
# Ensure vendors can view their own order details but not those of other vendors.
# Ensure vendors can manage their own warehouse quantity but cannot view or modify warehouse quantities of other vendors.
# Admin Users:
# Ensure admin users can view and update all product details, including warehouse quantities.
# Ensure admin users can view and edit all vendor details, including personal information.
# Ensure admin users can view and manage all orders and payments.
# Ensure admin users can manage user accounts, including authentication, permissions, and profiles.








