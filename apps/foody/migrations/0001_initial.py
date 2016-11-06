# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-06 02:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=25)),
                ('credit_card', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('buyer_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=25)),
                ('credit_card', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=200)),
                ('rating', models.FloatField(blank=True, default='5.0', null=True)),
                ('photo', models.URLField()),
                ('location', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('chef_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('price', models.FloatField()),
                ('rating', models.FloatField(blank=True, default='5.0', null=True)),
                ('description', models.TextField()),
                ('photo', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('belong_to_chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foody.Chef')),
            ],
            managers=[
                ('dish_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('user_name_reciever', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='foody.Chef')),
                ('user_name_sender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='foody.Buyer')),
            ],
        ),
        migrations.AddField(
            model_name='buyer',
            name='fav_chefs',
            field=models.ManyToManyField(to='foody.Chef'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='fav_dishes',
            field=models.ManyToManyField(to='foody.Dish'),
        ),
    ]