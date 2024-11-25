from django.urls import path
from .views import Userview

urlpatterns = [
    path('login/', Userview.as_view(), name='login'),
    path('logout/', Userview.as_view(), name='logout'),
    path('register/', Userview.as_view(), name='register'),
]