# Generated by Django 4.1.7 on 2024-10-14 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_bookings_delete_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
