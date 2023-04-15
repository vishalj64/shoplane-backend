
from django.urls import path

from shop import views

app_name = "shop"

urlpatterns = [
    path('', views.home, name="home"),
    path('api/products/', views.api_products, name="api_products"),
]