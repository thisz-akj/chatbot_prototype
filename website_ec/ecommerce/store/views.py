from django.shortcuts import render
from .models import Product, Order, OrderItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .serializers import OrderItemSerializer, ProductSerializer
import json

def store(request):
    customer = request.user.customer if request.user.is_authenticated else None
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all() if customer else []
    cartItems = order.get_cart_items if customer else 0

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    customer = request.user.customer if request.user.is_authenticated else None
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all() if customer else []
    cartItems = order.get_cart_items if customer else 0

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    customer = request.user.customer if request.user.is_authenticated else None
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all() if customer else []
    cartItems = order.get_cart_items if customer else 0

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@csrf_exempt
def updateItem(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            productId = data['productId']
            action = data['action']
            
            customer = request.user.customer if request.user.is_authenticated else None
            product = Product.objects.get(id=productId)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            
            if action == 'add':
                orderItem.quantity += 1
            elif action == 'remove':
                orderItem.quantity -= 1
            
            # Ensure the quantity does not drop below 0
            if orderItem.quantity <= 0:
                orderItem.delete()
            else:
                orderItem.save()
            
            return JsonResponse({'message': 'Item was updated successfully'}, safe=False)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'An error occurred'}, status=500, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405, safe=False)


from django.views.generic import ListView
from .models import Product

class ProductSearchView(ListView):
    model = Product
    template_name = 'store/search_results.html'  # You need to create this template
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Product.objects.filter(name__icontains=query).order_by('-id')
        return Product.objects.none()
