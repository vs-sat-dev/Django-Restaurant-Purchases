from rest_framework.routers import DefaultRouter

from .views import IngredientViewset, MenuItemViewset, RecipeRequirementViewset

router = DefaultRouter()

router.register('ingredient', IngredientViewset)
router.register('menu-item', MenuItemViewset)
router.register('recipe-requirement', RecipeRequirementViewset)

urlpatterns = router.urls
