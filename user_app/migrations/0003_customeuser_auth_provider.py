# Generated by Django 4.1.4 on 2023-01-17 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_alter_customeuser_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeuser',
            name='auth_provider',
            field=models.CharField(default='email', max_length=255),
        ),
    ]
