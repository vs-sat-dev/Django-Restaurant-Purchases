from rest_framework.routers import DefaultRouter

from .views import IngredientViewset

router = DefaultRouter()

router.register('ingredient', IngredientViewset)

urlpatterns = router.urls
