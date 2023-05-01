from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HomeView(APIView):
    def get(self, request):
        products = Product.objects.filter(active=True)
        categories = Category.objects.filter(active=True)
        serializer = ProductSerializer(products, many=True)
        data = {
            "products": serializer.data,
            "categories": [cat.name for cat in categories]
        }
        return Response(data, status=status.HTTP_200_OK)

class SearchView(APIView):
    def get(self, request):
        q = request.GET["q"]
        products = Product.objects.filter(active=True, name__icontains=q)
        serializer = ProductSerializer(products, many=True)
        data = {"products": serializer.data}
        return Response(data, status=status.HTTP_200_OK)

class CategoriesView(APIView):
    def get(self, request, slug):
        cat = Category.objects.get(slug=slug)
        products = Product.objects.filter(active=True, category=cat)
        serializer = ProductSerializer(products, many=True)
        data = {"products": serializer.data}
        return Response(data, status=status.HTTP_200_OK)

class DetailView(APIView):
    def get(self, request, slug):
        product = Product.objects.get(active=True, slug=slug)
        serializer = ProductSerializer(product)
        data = {"product": serializer.data}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        product = Product.objects.get(active=True, slug=slug)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review saved")
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        inital = {"items":[],"price":0.0,"count":0}
        session = request.session.get("data", inital)
        if slug in session["items"]:
            return Response({"error": "Already added to cart"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            session["items"].append(slug)
            session["price"] += float(product.price)
            session["count"] += 1
            request.session["data"] = session
            return Response({"success": "Added successfully"}, status=status.HTTP_200_OK)

class MyCartView(APIView):
    def get(self, request):
        sess = request.session.get("data", {"items":[]})
        products = Product.objects.filter(active=True, slug__in=sess["items"])
        serializer = ProductSerializer(products, many=True)
        data = {"products": serializer.data}
        return Response(data, status=status.HTTP_200_OK)

class CheckoutView(APIView):
    def get(self, request):
        request.session.pop('data', None)
        return Response(status=status.HTTP_200_OK)

class ApiProductsView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        products = Product.objects.filter(Q(name__contains=query) | Q(description__contains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SignupView(View):
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "User saved")
            return JsonResponse({"message": "User saved"})
        else:
            messages.error(request, "Error in form")
            return JsonResponse({"error": "Error in form"})


class SigninView(View):
    def post(self, request):
        form = SigninForm(request.POST)
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return JsonResponse({"message": "Successfully logged in"})
        else:
            messages.error(request, "Invalid Username or Password")
            return JsonResponse({"error": "Invalid Username or Password"})


class SignoutView(View):
    def get(self, request):
        logout(request)
        return JsonResponse({"message": "Successfully logged out"})
