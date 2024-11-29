from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Despesa, Receita
from .serializers import DespesaSerializer, ReceitaSerializer
from django.urls import path
from .views import get_despesas, get_receitas

class Despesa(models.Model):
    CATEGORIAS_DESPESAS = [
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('educacao', 'Educação'),
        ('moradia', 'Moradia'),
        ('saude', 'Saúde'),
        ('lazer', 'Lazer'),
        ('roupas', 'Roupas'),
        ('servicos', 'Serviços'),
        ('outros', 'Outros'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    valor = models.FloatField(default=0)
    data = models.DateField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_DESPESAS,default='Outros')                                                                                                                                                                                                                                                                                                                                                                       

    def __str__(self):
        return f'{self.descricao} - {self.valor} ({self.categoria})'

class Receita(models.Model):
    CATEGORIAS_RECEITAS = [
        ('salario', 'Salário'),
        ('freelancer', 'Freelancer'),
        ('investimentos', 'Investimentos'),
        ('presentes', 'Presentes'),
        ('aluguel', 'Aluguel'),
        ('venda_bens', 'Venda de Bens'),
        ('outros', 'Outros'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    valor = models.FloatField(default=0)
    data = models.DateField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_RECEITAS,default='Outros')

    def __str__(self):
        return f'{self.descricao} - {self.valor} ({self.categoria})'

@api_view(['GET'])
def get_despesas(request):
    despesas = Despesa.objects.all()
    serializer = DespesaSerializer(despesas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_receitas(request):
    receitas = Receita.objects.all()
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


urlpatterns = [
    path('despesas/', get_despesas, name='get_despesas'),
    path('receitas/', get_receitas, name='get_receitas'),
]
