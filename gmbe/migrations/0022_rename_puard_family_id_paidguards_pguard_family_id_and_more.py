# Generated by Django 4.1.6 on 2024-06-03 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gmbe', '0021_exchanges_shift_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paidguards',
            old_name='puard_family_id',
            new_name='pguard_family_id',
        ),
        migrations.RenameField(
            model_name='paidguards',
            old_name='puard_phone',
            new_name='pguard_phone',
        ),
    ]
