from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from .models import CartItem, get_cart_total, updateCartItemTotal
from accounts.models import Profile
from product.models import Product, Image, Variant
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
# go to the cart and list all items within the cart
@login_required(login_url=reverse_lazy('accounts:login'))
def index(request):
    # Get current users profile
    user_profile = Profile.objects.get(user=request.user)

    # Quantity is displayed in a user input form field, a POST request to this function updates quantity of the item in the cart
    if request.method == "POST":
        # Gather the cart items
        cart = CartItem.objects.filter(user=user_profile)
        # parse through the cart        
        for item in cart:
            # get each product form with the product id
            newQuantity = request.POST[f"product{item.variant.pk}"]
            print(item)
            print("Post Request: ", request.POST)
            # Only change the item quantity if the newquantity value is different
            if item.quantity != newQuantity:
                if int(newQuantity) <= 0:
                    deleteItem(request, item.items.id, item.variant.pk)
                else:
                    if int(newQuantity) > item.variant.stockAmount:
                        print("Big: ", int(newQuantity), ":", item.variant.stockAmount)
                        item.quantity = item.variant.stockAmount
                    else:    
                        item.quantity = int(newQuantity)
                    updateCartItemTotal(item)
                    item.save()
        
        # return a redirect to the index so when user refreshes it doesnt ask for a form resubmit
        return HttpResponseRedirect(reverse('cart:index'))
        
    # LOAD THE CART(GET)                
    # get all items in the cart associated with the profile
    cart = CartItem.objects.filter(user=user_profile)
    #Remember: totalPrice is part of the CartItem. So we do item.totalPrice. NOT item.items.totalPrice. That is going into the product

    for item in cart:
        if item.items.stockAmount == 0:
            deleteItem(request, item.items.id)

    cartList = []
    
    for item in cart:
        img = item.items.image_set.filter(isThumbnail=True).first()
        cartList.append({
            "item": item,

            "img": img.url  

        })

    # get the total value of the cart in its entirity
    cartTotal = get_cart_total(user_profile)

    # context to send to our html file
    context = {
        "cart": cartList,
        "cartTotal": cartTotal
    }

    return render(request, "cart/index.html", context)
    
# Function to add item to the cart
# - Takes arg id which is the id of the product to be added
@login_required(login_url=reverse_lazy('accounts:login'))
def itemAdded(request, id, **kwargs):
    #The html form automaticaly makes sure the quanity is atleast 1, and not a negative number
    profile = Profile.objects.get(user=request.user)#Get the profile instance from the db
    item = Product.objects.get(id=id) #Get the product from the products db
    
    try:
        quantity = request.GET["quantity"]#Get the quantity from the GET request
    except MultiValueDictKeyError as e:
        quantity = "1"
    print(request)
    variantPK = request.GET['options']
    print("printing variant " + variantPK)
    variant = Variant.objects.get(pk=variantPK) 
    print(variant)

    isAlreadyInCart = CartItem.objects.filter(user=profile, items=item, variant=variant) #This is a queryset that will have one object if the item is already gotten by the user
    if len(isAlreadyInCart) > 0:#If the user already bought the item
        cItemFromTable = isAlreadyInCart.first() #Make an instance of that CartItem that has the same product
        if cItemFromTable.quantity + int(quantity) > variant.stockAmount:#If the sum quantity is larget than stock, then make it so make amount can be added to cItem
            print("too high:", variant.stockAmount)
            cItemFromTable.quantity = variant.stockAmount
        else:
            cItemFromTable.quantity += int(quantity) #Increase it's quantity by the new amount

        updateCartItemTotal(cItemFromTable)#Now update this particular instance's totalPrice.
        cItemFromTable.save()#Save it back to the db

    else:#If the CartItem with the same product does not exist, make a new one
        if(int(quantity) > variant.stockAmount):#If quantity is larger than stock than make it equal to the max you can order
            quantity = variant.stockAmount
        cartItem = CartItem(
            user=profile,
            items=item, 
            quantity=quantity,
            variant=variant) #Create an instance of a CartItem with that item. Altough 'totalPrice' is a field of CartItem, it has a default and we are setting it right after this line anyways. We Have to set it after we make it.
        updateCartItemTotal(cartItem)#Now update this particular instance's totalPrice.
        cartItem.save() #Save it to the db
    print("Down here")
    return HttpResponseRedirect(reverse('cart:index')) #Give back a page saying added to cart

# Function to delete an item from the cart
def deleteItem(request, id, var):
    profile = Profile.objects.get(user=request.user)#Grab the profile and the item from the db
    item = Product.objects.get(id=id)
    variant = Variant.objects.get(pk=var)

    CartItem.objects.filter(user=profile, items=item, variant=variant).delete()#Find the cart item in the db and delete it
    
    #Return the cart page again
    return HttpResponseRedirect(reverse('cart:index'))


