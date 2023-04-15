from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.forms import ReviewForm, SignupForm, SigninForm
from shop.models import Product, Category
from shop.serializer import ProductSerializer


def home(request):
    products = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    context = {"products": products, "categories": categories}
    return render(request, "shop/home.html", context)


def search(request):
    q = request.GET["q"]
    products = Product.objects.filter(active=True, name__icontains=q)
    categories = Category.objects.filter(active=True)
    context = {"products": products,
               "categories": categories,
               "title": q + " - search"}
    return render(request, "shop/list.html", context)


def categories(request, slug):
    cat = Category.objects.get(slug=slug)
    products = Product.objects.filter(active=True, category=cat)
    categories = Category.objects.filter(active=True)
    context = {"products":products, "categories":categories, "title":cat.name + " - Categories"}
    return render(request, "shop/list.html", context)


def detail(request, slug):
    product = Product.objects.get(active=True, slug=slug)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review saved")
        else:
            messages.error(request, "Invalid form")
    else:
        form = ReviewForm()


    categories = Category.objects.filter(active=True)
    context = {"product" : product,
               "categories":categories,
               "form": form}
    return render(request, "shop/detail.html", context)



def cart(request, slug):
    """
        data = {"items" : ["slug1", "slug2"],
                "price" : 12342,
                "count" : 5
                }
        request.session["data"] = data
        """
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


def mycart(request):
    sess = request.session.get("data", {"items":[]})
    products = Product.objects.filter(active=True, slug__in=sess["items"])
    categories = Category.objects.filter(active=True)
    context = {"products": products,
               "categories": categories,
               "title": "My Cart"}
    return render(request, "shop/list.html", context)


def checkout(request):
    request.session.pop('data', None)
    return redirect("/")

@api_view(['GET'])
def api_products(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(Q(name__contains=query) | Q(description__contains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
