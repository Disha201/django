# Generated by Django 4.0.4 on 2022-06-27 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0007_merge_20220627_0312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discountedprice',
        ),
    ]
