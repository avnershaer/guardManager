# Generated by Django 4.1.6 on 2024-03-24 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gmbe', '0012_guardinglist_last_guard_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardinglist',
            name='last_guard_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='GuardingList_last_guard_id', to='gmbe.families'),
        ),
    ]
