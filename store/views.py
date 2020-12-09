from django.shortcuts import render
from product.models import Product, Image

# Create your views here.
def index(request):
    products = []
   # imgs = Product.objects.get(id=id).image_set.all()#Retrieve all the images related to this product
    for p in Product.objects.all()[:4]:
        products.append( {'product':p, 'img': p.image_set.filter(isThumbnail=True).first().url} )
        # products[p.pk] = {
        #     'product':p,
        #     'img': p.image_set.filter(isThumbnail=True).first().url
        # }
    print(products)
    return render(request, "store/index.html", {'context':products})
    

