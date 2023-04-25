

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.forms import ReviewForm, SignupForm, SigninForm
from shop.models import Product, Category
from shop.serializer import ProductSerializer

class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(active=True)
        categories = Category.objects.filter(active=True)
        context = {"products": products, "categories": categories}
        return render(request, "shop/home.html", context)


class SearchView(View):
    def get(self, request):
        q = request.GET["q"]
        products = Product.objects.filter(active=True, name__icontains=q)
        categories = Category.objects.filter(active=True)
        context = {"products": products,
                   "categories": categories,
                   "title": q + " - search"}
        return render(request, "shop/list.html", context)


class CategoriesView(View):
    def get(self, request, slug):
        cat = Category.objects.get(slug=slug)
        products = Product.objects.filter(active=True, category=cat)
        categories = Category.objects.filter(active=True)
        context = {"products": products, "categories": categories, "title": cat.name + " - Categories"}
        return render(request, "shop/list.html", context)


class DetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(active=True, slug=slug)
        form = ReviewForm()
        categories = Category.objects.filter(active=True)
        context = {"product": product,
                   "categories": categories,
                   "form": form}
        return render(request, "shop/detail.html", context)

    def post(self, request, slug):
        product = Product.objects.get(active=True, slug=slug)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review saved")
        else:
            messages.error(request, "Invalid form")
        categories = Category.objects.filter(active=True)
        context = {"product": product,
                   "categories": categories,
                   "form": form}
        return render(request, "shop/detail.html", context)


class CartView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        inital = {"items":[],"price":0.0,"count":0}
        session = request.session.get("data", inital)
        if slug in session["items"]:
            messages.error(request, "Already added to cart")
        else:
            session["items"].append(slug)
            session["price"] += float(product.price)
            session["count"] += 1
            request.session["data"] = session
            messages.success(request, "Added successfully")
        return redirect("shop:detail", slug)


class MyCartView(View):
    def get(self, request):
        sess = request.session.get("data", {"items":[]})
        products = Product.objects.filter(active=True, slug__in=sess["items"])
        categories = Category.objects.filter(active=True)
        context = {"products": products,
                   "categories": categories,
                   "title": "My Cart"}
        return render(request, "shop/list.html", context)


class CheckoutView(View):
    def get(self, request):
        request.session.pop('data', None)
        return redirect("/")



class ApiProductsView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        products = Product.objects.filter(Q(name__contains=query) | Q(description__contains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        context = {"form": form}
        return render(request, "shop/signup.html", context)

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "User saved")
            return redirect("shop:signin")
        else:
            messages.error(request, "Error in form")
        context = {"form": form}
        return render(request, "shop/signup.html", context)

class SigninView(View):
    def get(self, request):
        form = SigninForm()
        context = {"form": form}
        return render(request, "shop/signin.html", context)

    def post(self, request):
        form = SigninForm(request.POST)
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("shop:home")
        else:
            messages.error(request, "Invalid Username or Password")
        context = {"form": form}
        return render(request, "shop/signin.html", context)

class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect("shop:signin")
