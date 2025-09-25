# File: 0001_initial.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: file generated from migration of Porifle class

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.TextField(blank=True)),
                ("display_name", models.TextField(blank=True)),
                ("profile_image_url", models.TextField(blank=True)),
                ("bio_text", models.TextField(blank=True)),
                ("join_date", models.TextField(blank=True)),
            ],
        ),
    ]
