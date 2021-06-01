from django.contrib.auth.views import LoginView, logout_then_login
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout')
]
