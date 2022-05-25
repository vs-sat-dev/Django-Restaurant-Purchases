from django.urls import path

from .views import RegisterView, Login, Logout

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
