# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-03-13 00:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20190227_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsimage',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='goods.Goods'),
        ),
    ]
