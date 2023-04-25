from django.urls import path

from shop.views import (
    HomeView,
    SearchView,
    CartView,
    MyCartView,
    CheckoutView,
    DetailView,
    CategoriesView,
    ApiProductsView,
)

app_name = "shop"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('search/', SearchView.as_view(), name="search"),
    path('<slug>/cart/', CartView.as_view(), name="cart"),
    path('mycart/', MyCartView.as_view(), name="mycart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('<slug>/', DetailView.as_view(), name="detail"),
    path('categories/<slug>/', CategoriesView.as_view(), name="categories"),
    path('api/products/', ApiProductsView.as_view(), name="api_products"),
]
