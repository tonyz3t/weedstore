from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Title")
    
    def __str__(self): #This just displays the name instead of Product Object(1) or whatever
        return self.name

class Product(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=150)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    stockAmount = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

class Image(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    isThumbnail = models.BooleanField(default=True)

class Variant(models.Model):
    size = models.DecimalField(max_digits=5, decimal_places=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stockAmount = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return (self.product.name + " #" + str(self.size) + " $" + str(self.price) + " stock:" + str(self.stockAmount))