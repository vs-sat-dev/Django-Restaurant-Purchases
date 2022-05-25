from django.urls import path
from django.views.generic import TemplateView


app_name = 'restaurant'

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
]
