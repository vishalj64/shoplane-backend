
from django.urls import path

from shop import views
from .views import OrderItemsView, ReviewsByProductView, LoginAPIView
app_name = "shop"

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('search/', views.search, name="search"),
    path('<slug>/cart/', views.cart, name="cart"),
    path('mycart/', views.mycart, name="mycart"),
    path('checkout/', views.checkout, name="checkout"),
    path('<slug>/', views.detail, name="detail"),
    path('categories/<slug>/', views.categories, name="categories"),
    path('api/products/', views.api_products, name="api_products"),
    path('order-items/<int:order_id>/', OrderItemsView.as_view(), name='order-items'),
    path('reviews/<int:product_id>/', ReviewsByProductView.as_view(), name='reviews-by-product')
    path('api/token/', obtain_jwt_token),
    path('api/login/', LoginAPIView.as_view())
]
