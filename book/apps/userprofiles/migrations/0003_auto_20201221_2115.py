# Generated by Django 3.1.2 on 2020-12-21 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0002_auto_20201221_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='F:\\Disk\\HNEU\\Coursework\\Books\\book\\media\\avatarsprofile_image.png', upload_to='avatars'),
        ),
    ]