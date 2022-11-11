# Generated by Django 3.1.2 on 2020-12-05 23:05

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_remove_chapter_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='item_chapters_rus',
        ),
        migrations.AlterField(
            model_name='page',
            name='Chapter',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='item', chained_model_field='item', on_delete=django.db.models.deletion.CASCADE, related_name='page', to='items.chapter'),
        ),
    ]
