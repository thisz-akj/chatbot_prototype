from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import OrderItemViewSet, ProductViewSet, ProductSearchView

router = DefaultRouter()
router.register(r'orders', OrderItemViewSet, basename='orderitem')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Leave as empty string for base URL
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('search/', ProductSearchView.as_view(), name='search_product'),
    path('update_item/', views.updateItem, name='update_item'),
    path('api/', include(router.urls)),
]
