
from django.urls import path

from . import views

app_name = 'checkout'
urlpatterns = [
    path('', views.index, name="index"),
    path('pay/<int:pk>', views.pay, name="pay"),
    path('success', views.success, name="success"),
    path('cardError/<str:error>', views.cardError, name="cardError")

]