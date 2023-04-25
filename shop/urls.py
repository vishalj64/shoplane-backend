
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
    SignupView,
    SigninView,
    SignoutView
    
)

app_name = "shop"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('signin/', SigninView.as_view(), name="signin"),
    path('signout/', SignoutView.as_view(), name="signout"),
    path('search/', SearchView.as_view(), name="search"),
    path('<slug>/cart/', CartView.as_view(), name="cart"),
    path('mycart/', MyCartView.as_view(), name="mycart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('<slug>/', DetailView.as_view(), name="detail"),
    path('categories/<slug>/', CategoriesView.as_view(), name="categories"),
    path('api/products/', ApiProductsView.as_view(), name="api_products"),
]



    
   
