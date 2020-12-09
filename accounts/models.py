from django.conf import settings 
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

from product.models import Product
# Create your models here.

# CREATE A CUSTOM USER MODEL WHEN CREATING WEBSITES FOR ACTUAL CUSTOMERS
User = get_user_model()

# each user has a unique "profile" associated with them 
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # delete profile if user is deleted
    default_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, default=None)


    def __str__(self):
        return self.user.username
    
def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)

# Address
#   -   has user address and a foreign key pointing back to the user
class Address(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    address = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=7)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    

class PaymentMethod(models.Model):
    name_on_card = models.CharField(max_length=60)
    card_number = models.BigIntegerField()
    exp_date = models.IntegerField()
    