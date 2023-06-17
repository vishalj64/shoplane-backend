from django.http import JsonResponse
from django.views import View
from .models import Category, Product, Review
from django.core.paginator import Paginator
from django.db.models import Q

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


class ProductSearchAPI(View):
    def get(self, request):
        keyword = request.GET.get('keyword')
        products = Product.objects.filter(name__icontains=keyword)
        product_list = [product.name for product in products]
        return JsonResponse({'products': product_list})

class ProductFilterAPI(View):
    def get(self, request):
        category = request.GET.get('category')
        brand = request.GET.get('brand')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')

        products = Product.objects.filter(
            category__name=category,
            brand__icontains=brand,
            price__range=(price_min, price_max)
        )

        product_list = [product.name for product in products]
        return JsonResponse({'products': product_list})


class AllProductsAPI(View):
    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_list = [product.name for product in page_obj]
        next_page = page_obj.next_page_number() if page_obj.has_next() else None
        prev_page = page_obj.previous_page_number() if page_obj.has_previous() else None
        return JsonResponse({
            'products': product_list,
            'next_page': next_page,
            'prev_page': prev_page
        })

class ProductSearchPaginationAPI(View):
    def get(self, request):
        keyword = request.GET.get('keyword')
        products = Product.objects.filter(name__icontains=keyword)
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_list = [product.name for product in page_obj]
        next_page = page_obj.next_page_number() if page_obj.has_next() else None
        prev_page = page_obj.previous_page_number() if page_obj.has_previous() else None
        return JsonResponse({
            'products': product_list,
            'next_page': next_page,
            'prev_page': prev_page
        })
        
# Module 40 APIs-------------->

class PriceRangeSearchAPI(View):
    def get(self, request):
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
        data = [{'name': product.name, 'price': product.price} for product in products]

        return JsonResponse({'products': data})

class ProductFilterAPI(View):
    def get(self, request):
        category = request.GET.get('category')
        brand = request.GET.get('brand')
        availability = request.GET.get('availability')

        products = Product.objects.filter(
            Q(category__name=category) & Q(brand=brand) & Q(active=availability)
        )
        data = [{'name': product.name, 'brand': product.brand, 'active': product.active} for product in products]

        return JsonResponse({'products': data})

class ProductKeywordSearchAPI(View):
    def get(self, request):
        keyword = request.GET.get('keyword')

        products = Product.objects.mongo_find(
            {'$or': [
                {'name': {'$regex': keyword, '$options': 'i'}},
                {'description': {'$regex': keyword, '$options': 'i'}}
            ]}
        )
        data = [{'name': product.name, 'description': product.description} for product in products]

        return JsonResponse({'products': data})


class ProductKeywordSearchSingleIndexAPI(View):
    def get(self, request):
        keyword = request.GET.get('keyword')

        products = Product.objects.mongo_find(
            {'$or': [
                {'name': {'$regex': keyword, '$options': 'i'}},
                {'description': {'$regex': keyword, '$options': 'i'}}
            ]}
        ).hint([('name', 1)])  # Utilize the created index

        data = [{'name': product.name, 'description': product.description} for product in products]

        return JsonResponse({'products': data})


class ProductFilterCompoundIndexAPI(View):
    def get(self, request):
        category = request.GET.get('category')
        brand = request.GET.get('brand')
        availability = request.GET.get('availability')

        products = Product.objects.filter(
            Q(category__name=category) & Q(brand=brand) & Q(active=availability)
        ).hint([('category', 1), ('brand', 1)])  # Utilize the compound index

        data = [{'name': product.name, 'brand': product.brand, 'active': product.active} for product in products]

        return JsonResponse({'products': data})
