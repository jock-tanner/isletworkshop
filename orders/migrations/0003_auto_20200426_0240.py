# Generated by Django 2.2.12 on 2020-04-26 02:40

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200426_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=12, verbose_name='base price'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='local_price',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='local price'),
        ),
    ]
