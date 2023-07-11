# Generated by Django 4.2.2 on 2023-07-11 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smps', '0004_tower_assigned_alter_tower_contractor_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tower',
            name='contractor_id',
        ),
        migrations.AddField(
            model_name='tower',
            name='area_manager_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smps.user'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('long', models.DecimalField(decimal_places=6, max_digits=9)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smps.user')),
                ('tower_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smps.tower')),
            ],
        ),
    ]