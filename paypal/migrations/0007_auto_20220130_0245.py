# Generated by Django 3.1 on 2022-01-30 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paypal', '0006_auto_20220130_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paypalpayer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paypal_payer', to=settings.AUTH_USER_MODEL),
        ),
    ]
