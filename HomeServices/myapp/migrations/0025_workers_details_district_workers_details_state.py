# Generated by Django 5.1 on 2024-10-26 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_announcement'),
    ]

    operations = [
        migrations.AddField(
            model_name='workers_details',
            name='district',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='workers_details',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]