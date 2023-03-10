# Generated by Django 4.1.4 on 2022-12-28 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0003_contentwriterperformance_commentonblog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='reviewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_to_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
