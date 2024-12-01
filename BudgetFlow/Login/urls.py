from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registra/', RegisterView.as_view(), name='registra'),
    path('requisita_muda_senha/', RequestPasswordResetView.as_view(), name='requisita_muda_senha'),
    path('muda_senha/', ResetPasswordView.as_view(), name='muda_senha'),
    path('estalogado/',EstaLogadoView.as_view(), name='estalogado'),
]