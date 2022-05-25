from django.contrib import admin

from .models import Ingridient, MenuItem, RecipeRequirement, Purchase


admin.site.register(Ingridient)
admin.site.register(MenuItem)
admin.site.register(RecipeRequirement)
admin.site.register(Purchase)
