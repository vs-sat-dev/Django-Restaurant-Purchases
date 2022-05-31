from rest_framework.routers import DefaultRouter

from .views import IngredientViewset, MenuItemViewset, RecipeRequirementViewset, PurchaseViewset

router = DefaultRouter()

router.register('ingredient', IngredientViewset)
router.register('menu-item', MenuItemViewset)
router.register('recipe-requirement', RecipeRequirementViewset)
router.register('purchase', PurchaseViewset)

urlpatterns = router.urls
