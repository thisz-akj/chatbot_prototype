from rest_framework.routers import DefaultRouter
from store.urls import orderitem_router
from store.urls import product_router
from django.urls import path,include

router=DefaultRouter()

router.registry.extend(orderitem_router.registry)
router.registry.extend(product_router.registry)
urlpatterns=[
    path('',include(router.urls)),
]