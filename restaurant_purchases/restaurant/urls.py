from django.urls import path
from django.views.generic import TemplateView

from .views import IngridientList, MenuItemList, MenuItemDetail, RecipeRequirementList


app_name = 'restaurant'

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('ingridient-list/', IngridientList.as_view(), name='ingridient-list'),
    path('menu-item-list/', MenuItemList.as_view(), name='menu-item-list'),
    path('menu-item-detail/<int:pk>/', MenuItemDetail.as_view(), name='menu-item-detail'),
    path('recipe-requirement-list/', RecipeRequirementList.as_view(), name='recipe-requirement-list'),
]
