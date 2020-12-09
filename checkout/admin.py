from django.contrib import admin
from .models import Order, OrderJSON

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderJSON)