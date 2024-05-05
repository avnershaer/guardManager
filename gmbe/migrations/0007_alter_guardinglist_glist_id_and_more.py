# Generated by Django 4.1.6 on 2024-03-10 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gmbe', '0006_alter_setguardinglist_shifts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardinglist',
            name='glist_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='glistdetails_glist_id', to='gmbe.glistdetails'),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='setguardinglist',
            name='position_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='SetGuardingList_position_id', to='gmbe.position'),
        ),
    ]
