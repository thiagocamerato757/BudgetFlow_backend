from rest_framework import serializers
from .models import Receita, Despesa
from django.forms import ValidationError


class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = '__all__'
        
    def validate(self, data):
        if data['valor'] < 0:
            raise ValidationError('O valor da receita não pode ser negativo.')
        return data
    
class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = '__all__'
        
    def validate(self, data):
        if data['valor'] < 0:
            raise ValidationError('O valor da despesa não pode ser negativo.')
        return data