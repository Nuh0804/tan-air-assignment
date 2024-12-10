from .views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('carts', OrderViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', OrderItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls