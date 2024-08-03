from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from store.views import OrderItemViewSet, ProductViewSet

# Initialize the router for DRF
router = DefaultRouter()
router.register(r'orders', OrderItemViewSet, basename='orderitem')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Includes the URLs from your store app
    path('api/', include(router.urls)),  # Includes the DRF API URLs
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
