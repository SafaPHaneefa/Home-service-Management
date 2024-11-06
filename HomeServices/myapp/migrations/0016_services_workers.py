# Generated by Django 4.1.7 on 2024-10-18 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_image', models.ImageField(blank=True, null=True, upload_to='service_images/')),
                ('service_name', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_name', models.CharField(max_length=150)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('email', models.EmailField(max_length=150)),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('address', models.TextField()),
                ('pincode', models.CharField(max_length=150)),
                ('phone_no', models.CharField(max_length=15)),
                ('experience', models.CharField(max_length=150)),
                ('certificate', models.FileField(blank=True, null=True, upload_to='certificates/')),
                ('services', models.TextField()),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
