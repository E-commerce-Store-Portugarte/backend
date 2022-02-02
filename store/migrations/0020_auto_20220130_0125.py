# Generated by Django 3.1 on 2022-01-30 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0004_paypalpayer_user'),
        ('store', '0019_auto_20220130_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prepaymentorder',
            name='paypal_order_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='paypal.paypalorder'),
        ),
    ]
