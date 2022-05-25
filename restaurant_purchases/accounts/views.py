from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model

from .forms import RegisterForm


User = get_user_model()


class RegisterView(View):
    template_name = 'register.html'
    
    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context=context)
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return render(request, 'login.html')
        else:
            context = {'errors': form.errors, 'form': form}
            return render(request, 'register.html', context=context)
