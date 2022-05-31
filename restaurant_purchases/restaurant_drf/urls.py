from rest_framework.routers import DefaultRouter

from .views import IngredientViewset, MenuItemViewset

router = DefaultRouter()

router.register('ingredient', IngredientViewset)
router.register('menu-item', MenuItemViewset)

urlpatterns = router.urls
