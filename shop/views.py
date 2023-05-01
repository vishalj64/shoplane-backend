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




class ApiProductsView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        products = Product.objects.filter(Q(name__contains=query) | Q(description__contains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

