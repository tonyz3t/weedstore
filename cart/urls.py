from os import name
from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path("", views.index, name='index'),
    path('<int:id>/addToCart/', views.itemAdded, name="itemAdded" ),
    path('delete/<int:id>/<int:var>/', views.deleteItem, name='deleteItem'),
]