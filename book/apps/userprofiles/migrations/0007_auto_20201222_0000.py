# Generated by Django 3.1.2 on 2020-12-21 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0006_auto_20201221_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='avatars\\profile_image.png', upload_to='avatars'),
        ),
    ]
