from re import template
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.utils.timezone import now, timedelta
from django.middleware import csrf
import telegram
import requests
import json
from django.views.decorators.csrf import csrf_exempt

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
         for item in context['object_list']:
            recipe_requirements = RecipeRequirement.objects.filter(menu_item=item)
            print('MenuItemContext ', item.title)
            item.is_buy = True
            for recipe in recipe_requirements:
                if recipe.quantity > recipe.ingridient.quantity:
                    item.is_buy = False
                print('Ingridient: ', recipe.ingridient.quantity)
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
            #recipe['ingridient_quantity'] = ingridient.quantity
            recipe['ingridient'] = ingridient
        
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


@csrf_exempt
def send_telegram_message(message: str,
                            chat_id: str,
                            api_key: str,
                            csrf_token: str,
                            proxy_username: str = None,
                            proxy_password: str = None,
            proxy_url: str = None):
    responses = {}

    proxies = None
    headers = {'Content-Type': 'application/json',
                'Proxy-Authorization': 'Basic base64', 'X-CSRFToken': csrf_token}
    data_dict = {'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML',
                    'disable_notification': True}
    data = json.dumps(data_dict)
    url = f'https://api.telegram.org/bot{api_key}/sendMessage'
    response = requests.post(url, data=data, headers=headers, proxies=proxies, verify=False)
    print('Response: ', response)


@method_decorator(login_required, name='dispatch')
class MenuItemBuy(DetailView):
    model = MenuItem
    template_name = 'menu-item-buy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_requirements = RecipeRequirement.objects.filter(menu_item=context['object'])
        context['object'].is_buy = True
        for recipe in recipe_requirements:
            if recipe.quantity > recipe.ingridient.quantity:
                context['object'].is_buy = False
        return context

    def post(self, request, **kwargs):
        menu_item = get_object_or_404(MenuItem, pk=kwargs['pk'])
        if menu_item is not None:

            recipe_requirements = RecipeRequirement.objects.filter(menu_item=menu_item)
            is_buy = True
            ingridient_dict = {'ingridients': [], 'quantities': []}
            for recipe in recipe_requirements:
                ingridient_dict['quantities'].append(recipe.quantity)
                ingridient_dict['ingridients'].append(recipe.ingridient)
                if recipe.quantity > recipe.ingridient.quantity:
                    is_buy = False

            if is_buy:
                Purchase.objects.create(menu_item=menu_item, price=menu_item.price)
                for i in range(len(ingridient_dict)):
                    ingridient_dict['ingridients'][i].quantity = round(ingridient_dict['ingridients'][i].quantity - ingridient_dict['quantities'][i], 1)
                    ingridient_dict['ingridients'][i].save()
                #bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
                #bot.sendMessage(chat_id='241630970', text='My message')
                send_telegram_message(message='It was bouth', chat_id='241630970', 
                                      api_key='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw',
                                      csrf_token=csrf.get_token(self.request))
        
        return redirect('restaurant:menu-item-list')


@method_decorator(login_required, name='dispatch')
class PurchaseList(ListView):
    model = Purchase
    paginate_by = 3
    template_name = 'purchase-list.html'


@method_decorator(login_required, name='dispatch')
class IngridientUpdate(UpdateView):
    template_name = 'ingridient-update.html'
    form_class = IngridientForm
    model = Ingridient
    
    def get_success_url(self):
        view_name = 'update_mymodel'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse('restaurant:ingridient-list')


@method_decorator(login_required, name='dispatch')
class IngridientDelete(DetailView):
    model = Ingridient
    template_name = 'ingridient-delete.html'
    
    def post(self, request, *args, **kwargs):
        print('KWARGS: ', self.kwargs)
        ingridient = Ingridient.objects.get(pk=self.kwargs['pk'])
        if ingridient is not None:
            ingridient.delete()
        return redirect('restaurant:ingridient-list')


@method_decorator(login_required, name='dispatch')
class PurchaseCost(View):
    context_object_name = 'object'
    
    def get(self, request, *args, **kwargs):

        start = now().date()
        end = start + timedelta(days=1)

        today_purchases = Purchase.objects.filter(timestamp__range=(start, end))

        context = {'revenue': 0.0, 'costs': 0.0}
        for purchase in today_purchases:
            context['revenue'] += purchase.price

            recipe_requirements = RecipeRequirement.objects.filter(menu_item=purchase.menu_item)
            for recipe in recipe_requirements:
                context['costs'] += recipe.quantity * recipe.ingridient.unit_price
        
        context['costs'] = round(context['costs'], 1)
        context['profit'] = round(context['revenue'] - context['costs'], 1)

        return render(request, 'purchase-costs.html', context=context)
