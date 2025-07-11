# Generated by Django 5.2.2 on 2025-06-10 05:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=255)),
                ('contato', models.CharField(blank=True, max_length=255, null=True)),
                ('endereco', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=255)),
                ('contato', models.CharField(blank=True, max_length=255, null=True)),
                ('cnpj', models.CharField(blank=True, max_length=18, null=True)),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.DateField()),
                ('descricao', models.CharField(max_length=255)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.ForeignKey(limit_choices_to={'tipo': 'Despesa'}, on_delete=django.db.models.deletion.PROTECT, related_name='despesas', to='core.categoria')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='despesas', to='financial.fornecedor')),
            ],
            options={
                'verbose_name': 'Despesa',
                'verbose_name_plural': 'Despesas',
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='ContaPagarReceber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tipo', models.CharField(choices=[('Pagar', 'A Pagar'), ('Receber', 'A Receber')], max_length=10)),
                ('descricao', models.CharField(max_length=255)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_vencimento', models.DateField()),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Pago', 'Pago'), ('Atrasado', 'Atrasado'), ('Cancelado', 'Cancelado')], default='Pendente', max_length=10)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contas_receber', to='financial.cliente')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contas_pagar', to='financial.fornecedor')),
            ],
            options={
                'verbose_name': 'Conta a Pagar/Receber',
                'verbose_name_plural': 'Contas a Pagar/Receber',
                'ordering': ['data_vencimento'],
            },
        ),
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.DateField()),
                ('descricao', models.CharField(max_length=255)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.ForeignKey(limit_choices_to={'tipo': 'Receita'}, on_delete=django.db.models.deletion.PROTECT, related_name='receitas', to='core.categoria')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receitas', to='financial.cliente')),
            ],
            options={
                'verbose_name': 'Receita',
                'verbose_name_plural': 'Receitas',
                'ordering': ['-data'],
            },
        ),
    ]
