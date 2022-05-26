from django.urls import path
from django.views.generic import TemplateView

from .views import (
    IngridientList, MenuItemList, MenuItemDetail, RecipeRequirementList, MenuItemBuy,
    PurchaseList, IngridientUpdate, IngridientDelete
)


app_name = 'restaurant'

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('ingridient-list/', IngridientList.as_view(), name='ingridient-list'),
    path('ingridient-update/<int:pk>/', IngridientUpdate.as_view(), name='ingridient-update'),
    path('ingridient-delete/<int:pk>/', IngridientDelete.as_view(), name='ingridient-delete'),
    path('menu-item-list/', MenuItemList.as_view(), name='menu-item-list'),
    path('menu-item-detail/<int:pk>/', MenuItemDetail.as_view(), name='menu-item-detail'),
    path('menu-item-buy/<int:pk>/', MenuItemBuy.as_view(), name='menu-item-buy'),
    path('recipe-requirement-list/', RecipeRequirementList.as_view(), name='recipe-requirement-list'),
    path('purchase-list/', PurchaseList.as_view(), name='purchase-list'),
]
