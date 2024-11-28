# Generated by Django 3.2.25 on 2024-11-26 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('valor', models.FloatField(default=0)),
                ('data', models.DateField()),
                ('categoria', models.CharField(choices=[('salario', 'Salário'), ('freelancer', 'Freelancer'), ('investimentos', 'Investimentos'), ('presentes', 'Presentes'), ('aluguel', 'Aluguel'), ('venda_bens', 'Venda de Bens'), ('outros', 'Outros')], default='Outros', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('valor', models.FloatField(default=0)),
                ('data', models.DateField()),
                ('categoria', models.CharField(choices=[('alimentacao', 'Alimentação'), ('transporte', 'Transporte'), ('educacao', 'Educação'), ('moradia', 'Moradia'), ('saude', 'Saúde'), ('lazer', 'Lazer'), ('roupas', 'Roupas'), ('servicos', 'Serviços'), ('outros', 'Outros')], default='Outros', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]