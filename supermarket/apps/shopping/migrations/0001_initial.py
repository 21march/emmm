# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-29 08:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0003_auto_20180924_1923'),
        ('goods', '0002_auto_20180929_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='商品单价')),
                ('count', models.IntegerField(default=0, verbose_name='订单商品数')),
                ('goods_sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSKU', verbose_name='商品SKU')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('order_sn', models.CharField(max_length=255, verbose_name='订单编号')),
                ('order_money', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='订单金额')),
                ('recevier', models.CharField(max_length=100, verbose_name='收货人姓名')),
                ('recevier_phone', models.CharField(max_length=11, verbose_name='收货人电话')),
                ('address', models.CharField(max_length=255, verbose_name='收货人地址')),
                ('order_status', models.SmallIntegerField(choices=[(0, '待付款'), (1, '退发货'), (2, '待收货'), (3, '待评价'), (4, '已完成'), (5, '取消订单')], default=0, verbose_name='订单状态')),
                ('transport_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='运费')),
                ('pay_money', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='实际支付金额')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注说明')),
            ],
            options={
                'verbose_name': '订单基本信息表',
                'verbose_name_plural': '订单基本信息表',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('pay_name', models.CharField(max_length=20, verbose_name='支付方式')),
            ],
            options={
                'verbose_name': '支付方式',
                'verbose_name_plural': '支付方式',
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='配送方式')),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='金额')),
            ],
            options={
                'verbose_name': '配送方式',
                'verbose_name_plural': '配送方式',
            },
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopping.Payment', verbose_name='支付方式'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='transport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.Transport', verbose_name='运输方式'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User', verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.OrderInfo', verbose_name='所属订单'),
        ),
    ]