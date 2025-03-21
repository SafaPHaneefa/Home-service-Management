# Generated by Django 5.1 on 2025-03-14 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_workerlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerlocation',
            name='is_sharing',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='workerlocation',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='workerlocation',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
    ]
