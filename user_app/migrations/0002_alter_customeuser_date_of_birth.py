# Generated by Django 4.1.4 on 2022-12-28 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeuser',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]