# Generated by Django 3.1 on 2022-01-28 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
