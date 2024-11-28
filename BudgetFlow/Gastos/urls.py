from django.urls import path
from .views import *

urlpatterns = [
    path('Adiciona_despesa/', DespesaCreateView.as_view(), name='DespesaCreate'),
    path('Lista_despesas/', DespesaListView.as_view(), name='DespesaList'),
    path('Edita_desepesa/<int:pk>/', DespesaEditView.as_view(), name='DespesaEdit'),
    path('Deleta_despesa/<int:pk>/', DespesaDeleteView.as_view(), name='DespesaDelete'),
    path('Adiciona_receita/', ReceitaCreateView.as_view(), name='ReceitaCreate'),
    path('Lista_receitas/', ReceitaListView.as_view(), name='ReceitaList'),
    path('Edita_receita/<int:pk>/', ReceitaEditView.as_view(), name='ReceitaEdit'),
    path('Deleta_receita/<int:pk>/', ReceitaDeleteView.as_view(), name='ReceitaDelete'),
]