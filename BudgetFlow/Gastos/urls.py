from django.urls import path
from .views import *

urlpatterns = [
    path('Adiciona_despesa/', AdicionaDespesaView.as_view(), name='DespesaCreate'),
    path('Lista_despesas/', ListaDespesasView.as_view(), name='DespesaList'),
    path('Edita_despesa/<int:pk>/', EditaDespesaView.as_view(), name='DespesaEdit'),
    path('Deleta_despesa/<int:pk>/', DeletaDespesaView.as_view(), name='DespesaDelete'),
    path('Adiciona_receita/', AdicionaReceitaView.as_view(), name='ReceitaCreate'),
    path('Lista_receitas/', ListaReceitasView.as_view(), name='ReceitaList'),
    path('Edita_receita/<int:pk>/', EditaReceitaView.as_view(), name='ReceitaEdit'),
    path('Deleta_receita/<int:pk>/', DeletaReceitaView.as_view(), name='ReceitaDelete'),
]