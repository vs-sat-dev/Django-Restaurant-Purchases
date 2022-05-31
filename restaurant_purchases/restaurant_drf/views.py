from rest_framework import viewsets, mixins, permissions

from restaurant.models import Ingridient, MenuItem, RecipeRequirement, Purchase
from .serializers import IngredientSerializer, MenuItemSerializer, RecipeRequirementSerializer


class IngredientViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Ingridient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuItemViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class RecipeRequirementViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = RecipeRequirement.objects.all()
    serializer_class = RecipeRequirementSerializer
    permission_classes = [permissions.IsAuthenticated]
