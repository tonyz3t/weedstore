from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
import json

from .models import User, Profile, Address
from checkout.models import OrderJSON


# Create your views here.
@login_required(login_url=reverse_lazy('accounts:login'))
def index(request):
    return render(request, "accounts/index.html")

# View All Orders 
def order_list(request):
    user_profile = Profile.objects.get(user=request.user)
    orders = OrderJSON.objects.filter(user=user_profile).order_by('-id')
    context = {
        'items': []
    }
    for order in orders:
        context['items'].append(eval(order.data))
    
    return render(request, "accounts/orderList.html", context)

def login_view(request):
    # handle user login
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check to see if authentication was successful
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('accounts:index'))
        else:
            return render(request, "accounts/login.html", {
                "message": "Incorrect Username and/or Password"
            })

    if request.method == 'GET':
    # Send to accounts page if user already logged in
        if (request.user.is_authenticated):
            return HttpResponseRedirect(reverse('accounts:index'))

        return render(request, "accounts/login.html")

# User Logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:index'))

# User Registrations
def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']

        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, "accounts/register.html", {
                "message": "Passwords do not match"
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "accounts/register.html", {
                "message": "something went wrong"
            })
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse('accounts:index'))

    if request.method == 'GET':
        return render(request, "accounts/register.html")

def orderPage(request, id):
    user_profile = Profile.objects.get(user=request.user)
    order = OrderJSON.objects.get(orderID=id)
    context = {
        'order': eval(order.data)
    }
    return render(request, "accounts/orderPage.html", context)

def addressPage(request):
    user_profile = Profile.objects.get(user=request.user)
    addresses = Address.objects.filter(user=user_profile)

    # create context variable to send data with
    addressList = []

    for address in addresses:
        default = False
        
        if(user_profile.default_address == address):
            default = True

        addressList.append({ 'address': address, 'default': default })        

    return render(request, "accounts/addressPage.html", { 
        "addressess": addressList })

def newAddress(request):
    

    # Post Request
    if request.method == "POST":
        # User has submitted the form, retrieve its contents
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        address = request.POST["address"]
        zip_code = request.POST["zip_code"]
        
        user_profile = Profile.objects.get(user=request.user)

        # create address object
        address = Address(first_name=first_name, last_name=last_name, email=email, address=address, zip_code=zip_code, user=user_profile)
        address.save()
        # return user to addresspage
        return redirect('accounts:addressPage')

    return render(request, "accounts/newAddress.html")

def setDefault(request, id):
    user_profile = Profile.objects.get(user=request.user)
    user_profile.default_address = Address.objects.get(pk=id)
    user_profile.save()

    return redirect('accounts:addressPage')

# TODO: set default button
# TODO: add functions to allow user to change account settings
# TODO: store users payment information for easy orders
# TODO: Hash the password into the database for extra layer of security(maybe)
