# Generated by Django 4.1.6 on 2024-05-28 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gmbe', '0019_paidguards'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchanges',
            name='position_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='Exchanges_position_id', to='gmbe.position'),
        ),
    ]
