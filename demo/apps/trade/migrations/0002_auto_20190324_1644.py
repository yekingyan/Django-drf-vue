# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-03-24 16:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderGoods', to='trade.OrderInfo', verbose_name='订单'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_sn',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='订单号'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[set(['success', '成功']), set(['cancel', '取消']), set(['待支付', 'paying'])], default='paying', max_length=10, verbose_name='订单状态'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='post_script',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='订单留言'),
        ),
    ]
