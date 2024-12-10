from .views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('orders', OrderViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')

orders_router = routers.NestedDefaultRouter(router, 'orders', lookup='order')
orders_router.register('items', OrderItemViewSet, basename='order-items')

urlpatterns = router.urls + products_router.urls + orders_router.urls