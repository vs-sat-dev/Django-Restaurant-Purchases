from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from braces.views import SelectRelatedMixin

from .models import Ingridient, MenuItem, RecipeRequirement, Purchase
from .forms import IngridientForm, MenuItemForm, RecipeRequirementForm


@method_decorator(login_required, name='dispatch')
class IngridientList(ListView):
    model = Ingridient
    paginate_by = 3
    template_name = 'ingridient-list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['form'] = IngridientForm()
         return context
    
    def post(self, request):
        form = IngridientForm(request.POST)
        if form.is_valid():
            form.save()
            return super().get(request)
        else:
            context = {'errors': form.errors, 'form': form}
            return render(request, 'ingridient-post.html', context=context)


@method_decorator(login_required, name='dispatch')
class MenuItemList(ListView):
    model = MenuItem
    paginate_by = 3
    template_name = 'menu-item-list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['form'] = MenuItemForm()
         return context
    
    def post(self, request):
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return super().get(request)
        else:
            context = {'errors': form.errors, 'form': form}
            return render(request, 'menu-item-post.html', context=context)


@method_decorator(login_required, name='dispatch')
class MenuItemDetail(DetailView):
    model = MenuItem
    template_name = 'menu-item-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if "pk" in self.kwargs:
            menu_item = MenuItem.objects.get(id=self.kwargs['pk'])
            context['recipe_requirements'] = RecipeRequirement.objects.filter(menu_item=menu_item).values()
        
        for recipe in context['recipe_requirements']:
            ingridient = Ingridient.objects.get(id=recipe['ingridient_id'])
            recipe['name'] = ingridient.name
        
        context['form'] = RecipeRequirementForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        print('KWARGS: ', self.kwargs)
        form = RecipeRequirementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant:menu-item-detail', pk=self.kwargs['pk'])
        else:
            context = {'errors': form.errors, 'form': form}
            return render(request, 'menu-item-detail.html', context=context)


@method_decorator(login_required, name='dispatch')
class RecipeRequirementList(ListView):
    model = RecipeRequirement
    paginate_by = 3
    template_name = 'recipe-requirement-list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['form'] = RecipeRequirementForm()
         return context
    
    def post(self, request):
        form = RecipeRequirementForm(request.POST)
        if form.is_valid():
            form.save()
            return super().get(request)
        else:
            context = {'errors': form.errors, 'form': form}
            return render(request, 'recipe-requirement-post.html', context=context)

