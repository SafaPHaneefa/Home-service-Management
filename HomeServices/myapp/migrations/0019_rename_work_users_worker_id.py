# Generated by Django 4.1.7 on 2024-10-18 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_rename_services_service_details_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='work',
            new_name='worker_id',
        ),
    ]