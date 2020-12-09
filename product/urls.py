from django.urls import path
from . import views


app_name = 'product';#This is a namespace. So instead of calling reverse() and %url% like productIndex, it's product:index. Gets rid of name collisions
urlpatterns = [
    path('', views.productIndex, name="productIndex"),
    path('create', views.createProductView, name="createProduct"),
    path('<int:id>', views.productPage, name="productPage"),
    path('listCategories', views.listCategories, name="listCategories"),
    path('category/<int:id>', views.productsByCategory, name="productsByCategory")
]