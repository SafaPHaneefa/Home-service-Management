# Generated by Django 4.1.7 on 2024-10-23 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_rename_worker_id_bookings_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='workers_details',
            name='status',
            field=models.CharField(default='Available', max_length=100),
        ),
    ]
