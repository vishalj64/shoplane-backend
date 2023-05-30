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

class OrderItemsView(View):
    def get(self, request, order_id):
        order_items = OrderItem.objects.filter(order_id=order_id)
        order_item_list = []

        for order_item in order_items:
            order_item_data = {
                'id': order_item.id,
                'order_id': order_item.order_id,
                'product_id': order_item.product_id,
                'quantity': order_item.quantity,
                'price': order_item.price,
                # Add other fields as needed
            }
            order_item_list.append(order_item_data)

        return JsonResponse(order_item_list, safe=False)

class ReviewsByProductView(View):
    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        review_list = []

        for review in reviews:
            review_data = {
                'id': review.id,
                'product_id': review.product_id,
                'user_id': review.user_id,
                'rate': review.rate,
                'review': review.review,
                'created': review.created,
                'active': review.active
            }
            review_list.append(review_data)

        return JsonResponse(review_list, safe=False)
