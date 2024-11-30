from rest_framework import serializers
from .models import Receita, Despesa
from django.forms import ValidationError


class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'data', 'categoria']
        
    def validate(self, data):
        if data['valor'] < 0:
            raise ValidationError('O valor da receita não pode ser negativo.')
        return data
    def create(self, validated_data):
        # Corrige o nome do modelo e o campo de usuário
        usuario = self.context['request'].user
        return Receita.objects.create(user=usuario, **validated_data)
    
class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data', 'categoria']
        
    def validate(self, data):
        if data['valor'] < 0:
            raise ValidationError('O valor da despesa não pode ser negativo.')
        return data
    def create(self, validated_data):
        # Adiciona o usuário autenticado
        usuario = self.context['request'].user
        return Despesa.objects.create(user=usuario, **validated_data)