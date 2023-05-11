from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

users = []

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

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        mobile_number = data['mobile_number']
        password = data['password']

        # Create a new user and add it to the local array
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            mobile_number=mobile_number,
            password=password
        )
        users.append(user)

        return JsonResponse({'message': 'User signed up successfully'})
    
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        # Verify the user credentials in the local array
        user_found = False
        for user in users:
            if user.username == username and user.password == password:
                user_found = True
                break

        if user_found:
            return JsonResponse({'message': 'User signed in successfully'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

class SignOutView(View):
    def post(self, request):
        # Clear user session or perform additional tasks
        # Your implementation here

        return JsonResponse({'message': 'User signed out successfully'})
