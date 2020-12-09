from os import name
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("order/<int:id>/", views.orderPage, name="orderPage"),
    path("orders/", views.order_list, name="orderList"),
    path('addresses/', views.addressPage, name="addressPage"),
    path('addresses/new/', views.newAddress, name="newAddress"),
    path('addresses/default/<int:id>/', views.setDefault, name="setDefault"),
]