# Generated by Django 3.0.7 on 2020-07-24 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("itinerary", "0052_auto_20200706_1424"),
    ]

    operations = [
        migrations.CreateModel(
            name="Visit",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("description", models.CharField(max_length=255, null=True)),
                ("suggest_next_visit_day", models.BooleanField(null=True)),
                ("suggest_next_visit_evening", models.BooleanField(null=True)),
                ("suggest_next_visit_weekend", models.BooleanField(null=True)),
                ("suggest_next_visit_unknown", models.BooleanField(null=True)),
                ("suggest_discontinue_case", models.BooleanField(null=True)),
                (
                    "no_cooperation_malfunctioning_doorbell",
                    models.BooleanField(null=True),
                ),
                ("no_cooperation_video_call", models.BooleanField(null=True)),
                ("no_cooperation_hotel_furnished", models.BooleanField(null=True)),
                ("no_cooperation_vacant", models.BooleanField(null=True)),
                ("no_cooperation_likely_inhabited", models.BooleanField(null=True)),
                ("cooperation_likely_fraud", models.BooleanField(null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "itinerary_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="visits",
                        to="itinerary.ItineraryItem",
                    ),
                ),
            ],
        ),
    ]
