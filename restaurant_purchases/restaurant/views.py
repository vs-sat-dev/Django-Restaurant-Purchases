from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Ingridient, MenuItem, RecipeRequirement, Purchase
from .forms import IngridientForm, MenuItemForm


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
