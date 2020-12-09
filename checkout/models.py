from django.db import models
from random import randint

from cart.models import CartItem
from accounts.models import Profile
maxOrderID = 10000
# IN CHECKOUT WE WILL:
#   -   handle the checkout process
#   -   gather all the items from the cart
#   -   fill in user payment info
#   -   WHEN USER HITS THE CHECKOUT BUTTON WE WANT TO CREATE AN UNPAID ORDER WITH ALL THE CART ITEMS

# Model Functions

# Create your models here.  
# Order data table:
# - has a bunch of cartitems (manytomany)
# - has a relationship to the user who placed the order (foreignkey)
# - has a date when order is placed
# - an isOrdered property
# - - false: indicates that all the items are in the cart and have not been ordered
# - - true: indicates that all the items have been ordered and should no longer be shown in the cart
# - Payment details
# - Add an order status field (pending, recieved, shipping, delivered, etc)
class Order(models.Model):
    order_id = models.IntegerField()
    orderItems = models.ManyToManyField(CartItem)
    owner = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True)
    isOrdered = models.BooleanField(default=False) 
    
    @staticmethod
    def iID():#Make a static method that just makes sure the orderID is random
        r = randint(0, maxOrderID)#Initialize a random ID
        while(len(Order.objects.filter(order_id=r))) > 0:#Check if its in the db already
            print("DUPLICATE")
            r = randint(0, maxOrderID)#if yes, then make another one
        return r
    
    def __str__(self):
        return str(self.order_id)
    
    def get_order_items(self):
        return [item for item in self.orderItems.all()]

    def get_order_total(self):
        return sum([orderItem.totalPrice for orderItem in self.orderItems.all()])

    def serialize(self):
        return {
            "id": self.order_id,
            "orderItems": self.get_order_items(),
            "status": self.isOrdered,
            "orderTotal": self.get_order_total(),
            "primaryKey": self.pk
        }

    def serialize2(self):
        return {
            'id': self.order_id,
            'orderItems': [{'name': item.items.name, 'pk': item.items.pk, 'quantity': item.quantity, 'itemTotal': str(item.totalPrice)} for item in self.orderItems.all()],
            'status': self.isOrdered,
            'orderTotal': str(self.get_order_total()),
        }

# Our order json table
# ONLY STORE PAID FOR ORDERS IN HERE
class OrderJSON(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    data = models.TextField(null=True)
    orderID = models.IntegerField(null=True)
    def __str__(self):
        return self.user.user.username
    


