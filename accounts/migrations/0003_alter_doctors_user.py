# Generated by Django 4.2.6 on 2024-02-17 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_doctors_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctors",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="doctorss",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
