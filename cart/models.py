from django.db import models

from accounts.models import Profile
from product.models import Product, Variant

# Create your models here.

# Returns all items in a users cart
def get_cart_items(profile):
    return CartItem.objects.filter(user=profile).all()

# returns the total price of the entire cart
def get_cart_total(profile):
    cart_items = CartItem.objects.filter(user=profile).all()
    cart_total = 0
    for item in cart_items:
        cart_total += item.totalPrice #Now we can just use this.
        
    return cart_total
    
# CartItem data table:
# - has a bunch of products
class CartItem(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    items = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    totalPrice = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return (self.items.name + "," + str(self.quantity))

def updateCartItemTotal(cItem):#This function just takes in a CartItem, and updates it's totalPrice by multiplying quantity by price
    print(cItem.totalPrice)
    cItem.totalPrice = float(cItem.quantity) * float(cItem.items.price)

