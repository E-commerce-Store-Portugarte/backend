# Generated by Django 3.1 on 2022-01-30 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0005_auto_20220130_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paypalpurchaseunit',
            name='merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='paypal.paypalmerchant'),
        ),
    ]
