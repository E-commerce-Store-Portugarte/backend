# Generated by Django 4.0 on 2021-12-22 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('store', '0007_basketitems'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BasketItems',
            new_name='BasketItem',
        ),
    ]
