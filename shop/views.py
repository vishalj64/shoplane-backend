from django.http import JsonResponse
from django.views import View
from .models import Category, Product, Review

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all().values()
        return JsonResponse(list(categories), safe=False)

    def post(self, request):
        data = request.POST
        category = Category(
            name=data.get('name'),
            description=data.get('description'),
            featured=bool(data.get('featured')),
            active=bool(data.get('active'))
        )
        category.save()
        return JsonResponse({'message': 'Category created successfully'})

class ProductView(View):
    def get(self, request):
        products = Product.objects.all().values()
        return JsonResponse(list(products), safe=False)

    def post(self, request):
        data = request.POST
        product = Product(
            name=data.get('name'),
            brand=data.get('brand'),
            description=data.get('description'),
            price=float(data.get('price')),
            category_id=int(data.get('category')),
            featured=bool(data.get('featured')),
            active=bool(data.get('active'))
        )
        product.save()
        return JsonResponse({'message': 'Product created successfully'})

class ReviewView(View):
    def get(self, request):
        reviews = Review.objects.all().values()
        return JsonResponse(list(reviews), safe=False)

    def post(self, request):
        data = request.POST
        review = Review(
            product_id=int(data.get('product')),
            user_id=int(data.get('user')),
            rate=int(data.get('rate')),
            review=data.get('review'),
            active=bool(data.get('active'))
        )
        review.save()
        return JsonResponse({'message': 'Review created successfully'})
