# Generated by Django 3.2 on 2023-01-23 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_plan_app', '0011_auto_20230120_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='free_trail',
            field=models.BooleanField(default=False),
        ),
    ]
