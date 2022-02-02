# Generated by Django 3.1 on 2022-01-29 22:20

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20220128_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reference',
            field=models.UUIDField(default=store.models.generate_product_ref),
        ),
    ]
