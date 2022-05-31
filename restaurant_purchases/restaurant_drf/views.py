from rest_framework import viewsets, mixins, permissions

from restaurant.models import Ingridient, MenuItem, RecipeRequirement, Purchase
from .serializers import IngredientSerializer


class IngredientViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Ingridient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
