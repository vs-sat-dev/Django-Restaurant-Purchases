from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model

from .forms import RegisterForm, LoginForm


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
            return redirect('accounts:login')
        else:
            context = {'errors': form.errors, 'form': form}
            return render(request, 'register.html', context=context)


class Login(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_field_name = 'future'
    redirect_authenticated_user = True


class Logout(LogoutView):
    redirect_field_name = 'login'
