from django.urls import path
from shop.views import HomeView, ApiProductsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/products/', ApiProductsView.as_view(), name='api_products'),
]
