# Generated by Django 4.2.2 on 2023-07-12 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smps', '0007_alter_tower_area_manager_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tower',
            old_name='area_manager_id',
            new_name='area_manager',
        ),
    ]
