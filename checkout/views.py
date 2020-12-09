from checkout.models import Order, OrderJSON
from product.models import Product
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import stripe

from accounts.models import Profile, Address
from cart.models import CartItem


# Create your views here.

# starting page for our order
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    cart = CartItem.objects.filter(user=user_profile).all()

    # if the cart is empty, redirect the user back to the cart page
    if len(cart) <= 0:
        return HttpResponseRedirect(reverse('cart:index'))

    o = Order.objects.filter(owner=user_profile)
    print("Deleting: ")
    print(o)
    o.delete()
    print(o)
    # Create an unpaid for order for the user with their current cart
    order = Order(owner=user_profile, order_id=Order.iID())
    order.save()
    for product in cart:
        order.orderItems.add(product)
    
    # Grab the latest order
    #latest = Order.objects.get(owner=user_profile, isOrdered=False)
   
    # send this order to the order page
    context = {'obj' : order.serialize()}  # (see models.py) serialize creates a context object to be send with render request

    # return the checkout page
    return render(request, "checkout/index.html", context)

def pay(request, pk):
    user_profile = Profile.objects.get(user=request.user)
    address = user_profile.default_address
    order = Order.objects.get(pk=pk)

    if request.method == "POST":
        try:
            print("Order: " , pk, " Data: ", request.POST)
            print(order.owner, " ", order.isOrdered, " ", order.id, " total: ", order.get_order_total())

            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['nickname'],
                source=request.POST['stripeToken']
            )

            charge = stripe.Charge.create(
                customer=customer,
                amount = int(order.get_order_total() * 100),
                currency = 'usd',
                description='A charge'

            )

            order.isOrdered = True
            order.save()

            # Create serialized json data to save our order as a json field
            orderData = order.serialize2()
            orderJSON = OrderJSON(user=order.owner, data=orderData, orderID=order.order_id)
            orderJSON.save()

            # delete all the cartitems associated with this order
            itemsQuantities = {}
            # We need to add the new quantites into a dictionary with product id:newQuantity. The quantity could change while in checkout
            # so we check here if the quantities exceed the stockAmount. As soon as one does then we exit the function and return error. 
            # This makes it so the new quantity isn't saved to the database even if there is an error until we know all products' quantities 
            # dont exceed stock amount
            for item in CartItem.objects.filter(user=order.owner):#Go through all the products in the cart 
                if(item.items.stockAmount - item.quantity < 0):#If the new quantity is going to be a negative number
                    raise Exception("Quantity exceeds item stock")#Exit this with an error
                itemsQuantities[item.items.id] = item.items.stockAmount - item.quantity
                #Otherwise store the new temporary quantity in the dict. 
                # Because we don't know whether next product will raise error and we dont want to save the product's new quantity to the 
                # database prematurely
            for itemID in itemsQuantities.keys():#Now we know all products are safe to buy so loop through the product id's and update those product's quantites
                product = Product.objects.get(id=itemID)
                product.stockAmount = itemsQuantities[itemID]
                product.save()
            CartItem.objects.filter(user=order.owner).delete()#Finally delete all the cartItems

            return HttpResponseRedirect(reverse('checkout:success'))
        except Exception as e:
            return HttpResponseRedirect(reverse('checkout:cardError', kwargs={'error':e}))

    context = {
        "pk": pk,
        "obj": order.serialize(),
        "address": address,
    }
    
    return render(request, "checkout/pay.html", context)

def success(request):
    return render(request, "checkout/success.html")

def cardError(request, error):
    return render(request, "checkout/cardError.html", {'error':error})
# TODO: ability for user to checkout their order
# TODO: Handle payment
# TODO: store payment information
