# Generated by Django 3.1.2 on 2020-12-14 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_item_author'),
        ('library', '0002_auto_20201206_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='items',
            field=models.ManyToManyField(related_name='libraries', to='items.Item'),
        ),
    ]
