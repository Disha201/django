# Generated by Django 4.0.4 on 2022-06-11 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_product_discprice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='fname',
            new_name='name',
        ),
    ]
