from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .form import ProductModelForm
from .models import Product, Category, Image


# Create your views here.

def createProductView(request):
    print('outside ', request.method)
    if request.method == 'POST':
        productForm = ProductModelForm(request.POST)
        if productForm.is_valid():
            savedForm = productForm.save()
            #return redirect(reverse('product.views.createProductView'))
            print("Inside ")
            
            return redirect(reverse('product:productPage', kwargs={'id':savedForm.pk}))#pk means primary key. gives back primary key of the object in the db and directs to its product page
            
    else:
        productForm = ProductModelForm()
    context = {
        'form': productForm
    }
    
    return render(request, "product/createProduct.html", context)

# Returns product home page with all of the products
def productIndex(request):
    products = []

    for i in Product.objects.all():
        arr = []
        arr.append(i)
        img = i.image_set.filter(isThumbnail=True).first()
        arr.append(img.url)
        products.append(arr)

    print(products)
    return render(request, "product/index.html", {"products":products} )

# Function returns the view for a single item
# retrieves a page based on the items id
def productPage(request, **kwargs):
    # return the user to the page with single item
   
    imgsList = []#We need a list because we need to keep the order of the images. Thumbnails come first.

    imgs = Product.objects.get(id=kwargs['id']).image_set.all()#Retrieve all the images related to this product
    variants = Product.objects.get(id=kwargs['id']).variant_set.all()
    print(variants)

    for i in imgs:#Loop throuhg the images and if it is a thumbnail insert it at the beginning of the list otherwise at the end
        if i.isThumbnail:
            imgsList.insert(0, i.url)#Save space by only inserting the url at index 0
        else:
            imgsList.append(i.url)

    
    return render(request, "product/productPage.html", {
        "product": Product.objects.get(id=kwargs['id']),
        "images": imgsList,
        "variants": variants,
        
    })
    
def listCategories(request):#The view to show all the categories and their item lengths
    #Context dict has one key that has arrays inside of it with the category name, length of it's products, and the category id
    context = {
        'categories': []
    }
    
    # optimize this nested loop later if necessary runtime is O(n^2)
    for c in Category.objects.all():
        prods=[] 
        p = c.product_set.all()#This is a reverse search from parent to children. Get all 'product' in each category we iterate over and append an array that has the info

        for item in p:
            img = item.image_set.filter(isThumbnail=True).first()
            prods.append({ "p": item, "img": img.url})

        context['categories'].append([c.name, len(p), c.id, prods])#Append an array for each category

    return render(request, "product/listCategories.html", context)#Make these arrays here because the django template won't let you do all this stuff properly. So do all logic here and  just send array with info

def productsByCategory(request, id):#List all products in a category
    category = Category.objects.get(id=id)#Get the category we are searching in
    productsSet = category.product_set.all()#Reverse children from parent search. Get all of them in a queryset
    products = []

    for i in Category.objects.get(id=id).product_set.all():
        arr = []
        arr.append(i)
        img = i.image_set.filter(isThumbnail=True).first()
        arr.append(img.url)
        products.append(arr)
    print(products)
    return render(request, "product/productsByCategory.html", {'products': products, 'category': category})

#TODO
#Rename CartItem's 'items' to item.