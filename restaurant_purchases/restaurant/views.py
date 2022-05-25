from django.shortcuts import render
from django.views.generic import ListView

from .models import Ingridient


class IngridientList(ListView):
    model = Ingridient
    paginate_by = 3
    template_name = 'ingridient-list.html'
