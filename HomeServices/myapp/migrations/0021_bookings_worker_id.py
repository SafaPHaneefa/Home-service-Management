# Generated by Django 4.1.7 on 2024-10-23 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_service_details_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='worker_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='myapp.workers_details'),
        ),
    ]
